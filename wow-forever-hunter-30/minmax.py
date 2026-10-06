#!/usr/bin/env python3
"""Level 30 hunter PvP (duel) gear min-max for WoW Forever.

Duel model: you win when  your_EHP * your_DPS  >  their_EHP * their_DPS.
Their side is fixed, so the score to maximise is  ln(EHP) + ln(DPS):
1% more effective health is worth exactly as much as 1% more sustained damage.
Mana feeds DPS: shots run until you go OOM, then only Auto Shot is left.

Usage:
  python3 minmax.py weights            # value of each stat per point, plus Int vs Agi crossover
  python3 minmax.py slots [--top N]    # best items per slot
  python3 minmax.py set                # optimise a full gear set
  python3 minmax.py all
Edit config.json to calibrate the model, and items.csv / enchants.csv to add gear.
"""
import argparse
import csv
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STATS = ["agi", "sta", "int", "spi", "str", "ap", "rap", "mp5", "hit", "crit", "armor", "dps"]
SLOTS = ["head", "neck", "shoulder", "back", "chest", "wrist", "hands", "waist", "legs",
         "feet", "finger", "trinket", "main_hand", "off_hand", "two_hand", "ranged"]
DOUBLE_SLOTS = {"finger": 2, "trinket": 2}


def load_rows(path):
    if not os.path.exists(path):
        return []
    rows = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            if not r.get("name") or r["name"].startswith("#"):
                continue
            for s in STATS:
                v = (r.get(s) or "").strip()
                r[s] = float(v) if v else 0.0
            r["slot"] = r["slot"].strip().lower()
            r["unique"] = (r.get("unique") or "").strip().lower() in ("1", "y", "yes", "true")
            r["has_stats"] = any(r[s] for s in STATS)
            rows.append(r)
    return rows


class Model:
    def __init__(self, cfg):
        self.c = cfg["character"]
        self.t = cfg["talents"]
        self.r = cfg["ratings"]
        self.f = cfg["fight"]
        self.override = cfg.get("weights_override")

    def derived(self, g):
        """g: dict of gear stat totals. Returns the intermediate numbers."""
        c, t, r, f = self.c, self.t, self.r, self.f
        agi = c["naked_agi"] + g["agi"]
        sta = c["naked_sta"] + g["sta"]
        intel = c["naked_int"] + g["int"]
        spi = c["naked_spi"] + g["spi"]

        hp = (c["base_hp"] + sta * c["hp_per_sta"]) * c["hp_mult"]
        armor = c["base_armor"] + g["armor"] + agi * c["armor_per_agi"]
        armor_dr = armor / (armor + 400 + 85 * c["level"])
        dodge = min(agi / r["agi_per_dodge_pct"], 50) / 100
        phys = f["opponent_physical_frac"]
        taken = phys * (1 - armor_dr) * (1 - dodge) + (1 - phys)
        ehp = hp / taken

        L = f["duel_length_sec"]
        mana = c["base_mana"] + intel * c["mana_per_int"]
        mana += g["mp5"] * L / 5
        ticks_out = (L / 2) * f["fsr_out_frac"]
        mana += ticks_out * spi * f["spirit_mana_per_tick_per_spi"]

        rap = c["base_rap"] + agi + g["ap"] + g["rap"] + intel * 0.2 * t["careful_aim_ranks"]
        crit = (c["base_crit_pct"] + agi / r["agi_per_crit_pct"] + g["crit"]) / 100
        hit_mult = 1 - max(0.0, f["base_miss_pct"] - g["hit"]) / 100
        crit_mult = 1 + crit * (t["ranged_crit_damage_mult"] - 1)
        wdps = g["dps"] if g["dps"] else f["weapon_dps"]

        auto = (wdps + rap / f["ap_per_dps"]) * hit_mult * crit_mult
        shots = (f["shot_dps"] + rap * f["shot_ap_coeff"]) * hit_mult * crit_mult
        uptime = min(1.0, mana / (f["shot_mana_per_sec"] * L)) if f["shot_mana_per_sec"] else 1.0
        dps = auto + shots * uptime
        return dict(hp=hp, ehp=ehp, mana=mana, rap=rap, crit=crit * 100, dodge=dodge * 100,
                    armor=armor, dps=dps, uptime=uptime, oom_at=mana / f["shot_mana_per_sec"] if f["shot_mana_per_sec"] else float("inf"))

    def score(self, g):
        if self.override:
            return sum(self.override.get(s, 0) * g[s] for s in STATS)
        d = self.derived(g)
        return math.log(d["ehp"]) + math.log(d["dps"])


def zero():
    return {s: 0.0 for s in STATS}


def add(a, b, sign=1):
    return {s: a[s] + sign * b[s] for s in STATS}


def stat_weights(model, base):
    """Score gain per 1 point of each stat at gear totals `base`, normalised so Stamina = 1."""
    out = {}
    s0 = model.score(base)
    for s, step in [("sta", 10), ("agi", 10), ("int", 10), ("spi", 10), ("ap", 10),
                    ("mp5", 2), ("hit", 1), ("crit", 1), ("armor", 50), ("dps", 1)]:
        g = dict(base)
        g[s] += step
        out[s] = (model.score(g) - s0) / step
    ref = out["sta"] or 1
    return {k: v / ref for k, v in out.items()}


def best_set(model, items, enchants, exclude_unverified=False):
    pool = [i for i in items if i["has_stats"] and not (exclude_unverified and i.get("verified", "").lower() != "yes")]
    by_slot = {s: [i for i in pool if i["slot"] == s] for s in SLOTS}
    ench_by_slot = {s: [e for e in enchants if e["has_stats"] and e["slot"] == s] for s in SLOTS}

    positions = []
    for s in SLOTS:
        for n in range(DOUBLE_SLOTS.get(s, 1)):
            positions.append(s)
    chosen = {i: None for i in range(len(positions))}
    chosen_ench = {i: None for i in range(len(positions))}

    def totals():
        g = zero()
        for k in chosen:
            if chosen[k]:
                g = add(g, chosen[k])
            if chosen_ench[k] and chosen[k]:
                g = add(g, chosen_ench[k])
        return g

    def legal(k, item):
        s = positions[k]
        others = [chosen[j] for j in chosen if j != k and chosen[j]]
        if item["unique"] and any(o["name"] == item["name"] for o in others):
            return False
        if s == "two_hand" and any(positions[j] in ("main_hand", "off_hand") for j, o in chosen.items() if o and j != k):
            return False
        if s in ("main_hand", "off_hand") and any(positions[j] == "two_hand" for j, o in chosen.items() if o and j != k):
            return False
        return True

    for _ in range(20):
        changed = False
        for k, s in enumerate(positions):
            best, best_sc = chosen[k], None
            for cand in [None] + by_slot[s]:
                if cand and not legal(k, cand):
                    continue
                prev = chosen[k]
                chosen[k] = cand
                sc = model.score(totals())
                chosen[k] = prev
                if best_sc is None or sc > best_sc + 1e-12:
                    best, best_sc = cand, sc
            if best is not chosen[k]:
                chosen[k] = best
                changed = True
            if chosen[k]:
                be, be_sc = chosen_ench[k], None
                for e in [None] + ench_by_slot[s]:
                    prev = chosen_ench[k]
                    chosen_ench[k] = e
                    sc = model.score(totals())
                    chosen_ench[k] = prev
                    if be_sc is None or sc > be_sc + 1e-12:
                        be, be_sc = e, sc
                if be is not chosen_ench[k]:
                    chosen_ench[k] = be
                    changed = True
        if not changed:
            break
    return positions, chosen, chosen_ench, totals()


def fmt_stats(i):
    return ", ".join(f"{i[s]:+g} {s}" for s in STATS if i[s])


def cmd_weights(model, base):
    w = stat_weights(model, base)
    d = model.derived(base)
    print(f"At current gear: HP {d['hp']:.0f}  EHP {d['ehp']:.0f}  mana {d['mana']:.0f}  RAP {d['rap']:.0f}  "
          f"crit {d['crit']:.1f}%  DPS {d['dps']:.1f}  shot uptime {d['uptime']*100:.0f}% (OOM at {d['oom_at']:.0f}s)")
    print("\nValue per point (Stamina = 1.00):")
    for k, v in sorted(w.items(), key=lambda kv: -kv[1]):
        print(f"  {k:6s} {v:6.2f}")

    print("\nInt vs Agi vs Sta as duel length changes:")
    print("  duel_s  sta   agi   int   spi   mp5  | winner")
    L0 = model.f["duel_length_sec"]
    cross = None
    for L in (20, 30, 45, 60, 75, 90, 120, 150, 180):
        model.f["duel_length_sec"] = L
        ww = stat_weights(model, base)
        top = max(("sta", "agi", "int"), key=lambda k: ww[k])
        print(f"  {L:5d}  {ww['sta']:.2f}  {ww['agi']:.2f}  {ww['int']:.2f}  {ww['spi']:.2f}  {ww['mp5']:.2f}  | {top}")
        if cross is None and ww["int"] > ww["agi"]:
            cross = L
    model.f["duel_length_sec"] = L0
    if cross:
        print(f"\nInt passes Agi once duels last about {cross}s or more (you start running out of mana before the kill).")
    else:
        print("\nAgi stays ahead of Int at every tested duel length with these settings.")


def cmd_slots(model, items, enchants, base, top):
    missing = [i["name"] for i in items if not i["has_stats"]]
    for s in SLOTS:
        rows = [i for i in items if i["slot"] == s and i["has_stats"]]
        erows = [e for e in enchants if e["slot"] == s and e["has_stats"]]
        if not rows and not erows:
            continue
        print(f"\n== {s} ==")
        s0 = model.score(base)
        ranked = sorted(rows, key=lambda i: -(model.score(add(base, i)) - s0))
        for i in ranked[:top]:
            gain = model.score(add(base, i)) - s0
            flag = "" if i.get("verified", "").lower() == "yes" else "  [unverified]"
            print(f"  {gain*1000:6.1f}  {i['name']:<36} {fmt_stats(i)}  ({i.get('source','')}){flag}")
        for e in sorted(erows, key=lambda e: -(model.score(add(base, e)) - s0))[:3]:
            print(f"  ench {(model.score(add(base, e)) - s0)*1000:5.1f}  {e['name']:<31} {fmt_stats(e)}")
    if missing:
        print(f"\n{len(missing)} items in items.csv have no stats filled in yet: " + "; ".join(missing))
    print("\n(score = duel score gain x1000 from adding the item to the baseline in base_gear.json)")


def cmd_set(model, items, enchants, exclude_unverified):
    positions, chosen, ench, g = best_set(model, items, enchants, exclude_unverified)
    print("\nOptimised set:")
    for k, s in enumerate(positions):
        it = chosen[k]
        e = ench[k]
        name = it["name"] if it else "-"
        extra = f"  + {e['name']}" if e else ""
        print(f"  {s:10s} {name}{extra}")
    d = model.derived(g)
    print(f"\nTotals from gear: {fmt_stats(g)}")
    print(f"HP {d['hp']:.0f}  EHP {d['ehp']:.0f}  mana {d['mana']:.0f}  RAP {d['rap']:.0f}  crit {d['crit']:.1f}%  "
          f"dodge {d['dodge']:.1f}%  DPS {d['dps']:.1f}  shot uptime {d['uptime']*100:.0f}%")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["weights", "slots", "set", "all"])
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--verified-only", action="store_true", help="ignore items not marked verified=yes")
    ap.add_argument("--duel", type=float, help="override duel_length_sec")
    ap.add_argument("--config", default=os.path.join(HERE, "config.json"))
    a = ap.parse_args()

    cfg = json.load(open(a.config))
    if a.duel:
        cfg["fight"]["duel_length_sec"] = a.duel
    model = Model(cfg)
    items = load_rows(os.path.join(HERE, "items.csv"))
    enchants = load_rows(os.path.join(HERE, "enchants.csv"))
    base = zero()
    bpath = os.path.join(HERE, "base_gear.json")
    if os.path.exists(bpath):
        base.update({k: float(v) for k, v in json.load(open(bpath)).items() if k in STATS})

    if a.cmd in ("weights", "all"):
        cmd_weights(model, base)
    if a.cmd in ("slots", "all"):
        cmd_slots(model, items, enchants, base, a.top)
    if a.cmd in ("set", "all"):
        cmd_set(model, items, enchants, a.verified_only)


if __name__ == "__main__":
    sys.exit(main())
