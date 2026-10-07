#!/usr/bin/env python3
"""Stress test: is the balanced (model-optimised) set really better than stacking one stat?

Builds four sets from the same item pool:
  balanced  - minmax.py's optimiser (EHP x DPS)
  agi       - maximise Agility (Stamina as tiebreak)
  sta       - maximise Stamina (Agility as tiebreak)
  int       - maximise Intellect (Stamina as tiebreak)
then scores every set under many "what if my assumptions are wrong" scenarios.

Usage: python3 stress_test.py [--build sv_mm_tank] [--faction horde]
"""
import argparse
import copy
import json
import os
import sys

import minmax  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

STACKS = {
    "agi": {"agi": 1.0, "sta": 0.05, "ap": 0.02, "dps": 0.5},
    "sta": {"sta": 1.0, "agi": 0.05, "dps": 0.5},
    "int": {"int": 1.0, "sta": 0.05, "dps": 0.5},
    "agi_lean": {"agi": 1.0, "sta": 0.5, "ap": 0.4, "dps": 2.0},
    "classic": {"sta": 1.0, "agi": 0.7, "ap": 0.35, "dps": 2.0},
}

SCENARIOS = [
    ("baseline (placeholders)", {}),
    ("Agi gives 2x crit (15 agi/1%)", {"ratings.agi_per_crit_pct": 15}),
    ("Agi gives little crit (45 agi/1%)", {"ratings.agi_per_crit_pct": 45}),
    ("full MM crit dmg (Mortal Shots)", {"builds.{b}.ranged_crit_damage_mult": 2.3}),
    ("short duel 30s", {"matchups.generic.duel_sec": 30}),
    ("long duel 120s (priest-like)", {"matchups.generic.duel_sec": 120}),
    ("vs physical (rogue/warrior)", {"matchups.generic.physical_frac": 0.95, "matchups.generic.duel_sec": 35}),
    ("vs caster (mage/lock)", {"matchups.generic.physical_frac": 0.05, "matchups.generic.duel_sec": 45}),
    ("mana shots are weak (shot_dps 10)", {"rotation.shot_dps": 10}),
    ("mana shots are strong (shot_dps 45)", {"rotation.shot_dps": 45}),
    ("no pet (pet_dps 0)", {"rotation.pet_dps": 0}),
    ("higher base HP (900)", {"character.base_hp": 900}),
]


def apply(cfg, changes, build):
    c = copy.deepcopy(cfg)
    for path, v in changes.items():
        node = c
        parts = path.replace("{b}", build).split(".")
        for p in parts[:-1]:
            node = node[p]
        node[parts[-1]] = v
    return c


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--build", default="sv_mm_tank")
    ap.add_argument("--faction", default="horde")
    a = ap.parse_args()

    cfg = json.load(open(os.path.join(HERE, "config.json")))
    cfg["filters"]["faction"] = a.faction
    minmax.ALLOW_DUPLICATES = cfg["filters"].get("allow_duplicate_items", False)
    items = minmax.load_rows(os.path.join(HERE, "items.csv"), cfg["filters"])
    items += minmax.load_rows(os.path.join(HERE, "items_manual.csv"), cfg["filters"])
    enchants = minmax.load_rows(os.path.join(HERE, "enchants.csv"))

    sets = {}
    sets["balanced"] = minmax.best_set(minmax.Model(cfg, a.build, "generic"), items, enchants)[3]
    for name, w in STACKS.items():
        c = copy.deepcopy(cfg)
        c["weights_override"] = w
        sets[name] = minmax.best_set(minmax.Model(c, a.build, "generic"), items, enchants)[3]

    print(f"build {a.build}, faction {a.faction}\n")
    print("Gear totals per set:")
    for n, g in sets.items():
        d = minmax.Model(cfg, a.build, "generic").derived(g)
        print(f"  {n:9s} agi {g['agi']:4.0f} sta {g['sta']:4.0f} int {g['int']:4.0f} ap {g['ap']:4.0f} dps {g['dps']:5.1f}"
              f"  ->  HP {d['hp']:5.0f}  mana {d['mana']:5.0f}  RAP {d['rap']:4.0f}  crit {d['crit']:4.1f}%")

    print("\nWin power (EHP x DPS) relative to the balanced set, per scenario. >100% = beats balanced.")
    print(f"{'scenario':38s}" + "".join(f"{n:>10s}" for n in sets))
    wins = {n: 0 for n in sets}
    for label, ch in SCENARIOS:
        c = apply(cfg, ch, a.build)
        m = minmax.Model(c, a.build, "generic")
        vals = {}
        for n, g in sets.items():
            d = m.derived(g)
            vals[n] = d["ehp"] * d["dps"]
        ref = vals["balanced"]
        best = max(vals, key=vals.get)
        wins[best] += 1
        print(f"{label:38s}" + "".join(f"{vals[n] / ref * 100:9.0f}%" for n in sets) + f"   best: {best}")
    print("\nScenarios won: " + ", ".join(f"{n} {w}" for n, w in wins.items()))

    print("\nDifferent scoring: what if only one side of the race matters?")
    m = minmax.Model(cfg, a.build, "generic")
    for label, key in (("pure damage (DPS)", "dps"), ("pure survival (EHP)", "ehp")):
        vals = {n: m.derived(g)[key] for n, g in sets.items()}
        ref = vals["balanced"]
        print(f"{label:38s}" + "".join(f"{vals[n] / ref * 100:9.0f}%" for n in sets) + f"   best: {max(vals, key=vals.get)}")

    print("\nWhat each set means in a duel (baseline): time to kill a 3,000-EHP target / time to survive 70 DPS")
    m = minmax.Model(cfg, a.build, "generic")
    for n, g in sets.items():
        d = m.derived(g)
        print(f"  {n:9s} kills in {3000 / d['dps']:5.1f}s   survives {d['ehp'] / 70:5.1f}s   margin {d['ehp'] / 70 - 3000 / d['dps']:+5.1f}s")


if __name__ == "__main__":
    main()
