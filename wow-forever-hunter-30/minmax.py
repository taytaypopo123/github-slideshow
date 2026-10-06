#!/usr/bin/env python3
"""Level 30 hunter PvP (duel) gear min-max for WoW Forever.

Duel model: you win when  your_EHP * your_DPS  >  their_EHP * their_DPS.
Their side is fixed, so the score to maximise is  ln(EHP) + ln(DPS):
1% more effective health is worth exactly as much as 1% more sustained damage.
Mana feeds DPS: shots run until you go OOM, then only Auto Shot (and your pet) is left.

Usage:
  python3 minmax.py matrix                       # Sta/Agi/Int value for every build x matchup
  python3 minmax.py weights [--build B --vs M]   # all stat values, plus duel-length crossover
  python3 minmax.py slots   [--build B --vs M] [--top N]
  python3 minmax.py set     [--build B --vs M]   # optimise a full gear set
  python3 minmax.py compare [--vs M]             # best set for each build, scored against each other
Builds and matchups live in config.json. Gear lives in items.csv / enchants.csv.
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
ALLOW_DUPLICATES = False  # set from config filters.allow_duplicate_items
# one-hand weapons can go in either hand
FITS = {s: {s} for s in SLOTS}
FITS["main_hand"] = {"main_hand", "one_hand"}
FITS["off_hand"] = {"off_hand", "one_hand"}


def num(v):
    v = (v or "").strip()
    return float(v) if v else 0.0


def load_rows(path, filters=None):
    if not os.path.exists(path):
        return []
    f = filters or {}
    rows = []
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            if not r.get("name") or r["name"].startswith("#"):
                continue
            for s in STATS:
                r[s] = num(r.get(s))
            r["slot"] = r["slot"].strip().lower()
            r["unique"] = (r.get("unique") or "").strip().lower() in ("1", "y", "yes", "true")
            r["has_stats"] = any(r[s] for s in STATS)
            if filters is not None:
                if not f.get("allow_mail", False) and r.get("armor_type") == "mail":
                    continue
                if r.get("quality") and int(r["quality"]) < f.get("min_quality", 0):
                    continue
                if r.get("req_level") and int(float(r["req_level"])) > f.get("max_req_level", 999):
                    continue
                if any(n and n in (r.get("notes") or "") for n in f.get("exclude_notes", [])):
                    continue
                if not f.get("allow_no_req_high_ilvl", False) and "no level req, high item level" in (r.get("notes") or ""):
                    continue
                side = (r.get("faction") or "").strip().lower()
                if side and f.get("faction", "any") not in ("any", side):
                    continue
            rows.append(r)
    return rows


class Model:
    def __init__(self, cfg, build, matchup):
        self.c = cfg["character"]
        self.r = cfg["ratings"]
        self.rot = cfg["rotation"]
        self.b = cfg["builds"][build]
        self.m = dict(cfg["matchups"][matchup])
        self.override = cfg.get("weights_override")

    def derived(self, g):
        c, r, rot, b, m = self.c, self.r, self.rot, self.b, self.m
        agi = c["naked_agi"] + g["agi"]
        sta = c["naked_sta"] + g["sta"]
        intel = c["naked_int"] + g["int"]
        spi = c["naked_spi"] + g["spi"]

        hp = (c["base_hp"] + sta * c["hp_per_sta"]) * c["race_hp_mult"] * b["hp_mult"]
        armor = c["base_armor"] + g["armor"] + agi * c["armor_per_agi"]
        armor_dr = armor / (armor + 400 + 85 * c["level"])
        dodge = min(agi / r["agi_per_dodge_pct"], 50) / 100
        phys = m["physical_frac"]
        ehp = hp / (phys * (1 - armor_dr) * (1 - dodge) + (1 - phys))

        L = m["duel_sec"]
        mana = c["base_mana"] + intel * c["mana_per_int"] + g["mp5"] * L / 5
        mana += (L / 2) * rot["fsr_out_frac"] * spi * rot["spirit_mana_per_tick_per_spi"]

        rap = c["base_rap"] + agi + g["ap"] + g["rap"] + intel * 0.2 * b["careful_aim_ranks"]
        crit = (c["base_crit_pct"] + b["crit_bonus_pct"] + agi / r["agi_per_crit_pct"] + g["crit"]) / 100
        hit_mult = 1 - max(0.0, rot["base_miss_pct"] - g["hit"]) / 100
        crit_mult = 1 + min(crit, 1) * (b["ranged_crit_damage_mult"] - 1)
        wdps = g["dps"] or rot["weapon_dps"]

        auto = (wdps + rap / rot["ap_per_dps"]) * hit_mult * crit_mult
        shots = (rot["shot_dps"] + rap * rot["shot_ap_coeff"]) * hit_mult * crit_mult
        spend = rot["shot_mana_per_sec"] * b["mana_cost_mult"]
        uptime = min(1.0, mana / (spend * L)) if spend else 1.0
        pet = rot["pet_dps"] * b["pet_dps_mult"]
        dps = (auto + shots * uptime) * b["dmg_mult"] + pet
        return dict(hp=hp, ehp=ehp, mana=mana, rap=rap, crit=crit * 100, dodge=dodge * 100, armor=armor,
                    dps=dps, uptime=uptime, oom_at=mana / spend if spend else float("inf"))

    def score(self, g):
        if self.override:
            return sum(self.override.get(s, 0) * g[s] for s in STATS)
        d = self.derived(g)
        return math.log(d["ehp"]) + math.log(d["dps"])


def zero():
    return {s: 0.0 for s in STATS}


def add(a, b):
    return {s: a[s] + b[s] for s in STATS}


def stat_weights(model, base):
    """Score gain per point of each stat at gear totals `base`, normalised so Stamina = 1."""
    out = {}
    s0 = model.score(base)
    for s, step in [("sta", 10), ("agi", 10), ("int", 10), ("spi", 10), ("ap", 10),
                    ("mp5", 2), ("hit", 1), ("crit", 1), ("armor", 50), ("dps", 1)]:
        g = dict(base)
        g[s] += step
        out[s] = (model.score(g) - s0) / step
    ref = out["sta"] or 1
    return {k: v / ref for k, v in out.items()}


def best_set(model, items, enchants):
    pool = [i for i in items if i["has_stats"]]
    by_pos = {s: [i for i in pool if i["slot"] in FITS[s]] for s in SLOTS}
    ench_by_slot = {s: [e for e in enchants if e["has_stats"] and e["slot"] == s] for s in SLOTS}
    positions = [s for s in SLOTS for _ in range(DOUBLE_SLOTS.get(s, 1))]
    chosen = [None] * len(positions)
    chosen_ench = [None] * len(positions)

    def totals():
        g = zero()
        for k, it in enumerate(chosen):
            if it:
                g = add(g, it)
                if chosen_ench[k]:
                    g = add(g, chosen_ench[k])
        return g

    def legal(k, item):
        s = positions[k]
        for j, o in enumerate(chosen):
            if j == k or not o:
                continue
            if o.get("wowhead_id", o["name"]) == item.get("wowhead_id", item["name"]) and (
                    item["unique"] or not ALLOW_DUPLICATES):
                return False
            fa, fb = (item.get("faction") or "").strip(), (o.get("faction") or "").strip()
            if fa and fb and fa != fb:
                return False
            if s == "two_hand" and positions[j] in ("main_hand", "off_hand"):
                return False
            if s in ("main_hand", "off_hand") and positions[j] == "two_hand":
                return False
        return True

    def pick(k, options, cur, setter):
        best, best_sc = cur, None
        for cand in [None] + options:
            setter(k, cand)
            sc = model.score(totals())
            if best_sc is None or sc > best_sc + 1e-12:
                best, best_sc = cand, sc
        setter(k, best)
        return best is not cur

    def set_item(k, v): chosen[k] = v
    def set_ench(k, v): chosen_ench[k] = v

    for _ in range(25):
        changed = False
        for k, s in enumerate(positions):
            opts = [i for i in by_pos[s] if legal(k, i)]
            changed |= pick(k, opts, chosen[k], set_item)
            if chosen[k]:
                changed |= pick(k, ench_by_slot[s], chosen_ench[k], set_ench)
            else:
                chosen_ench[k] = None
        if not changed:
            break
    return positions, chosen, chosen_ench, totals()


def fmt_stats(i):
    return ", ".join(f"{i[s]:+g} {s}" for s in STATS if i[s])


def link(i):
    wid = (i.get("wowhead_id") or "").strip()
    if not wid:
        return ""
    b = (i.get("bonus") or "").strip()
    return f"https://www.wowhead.com/forever/item={wid}" + (f"?bonus={b}" if b else "")


def cmd_matrix(cfg, base):
    builds = [b for b in cfg["builds"] if not b.startswith("_")]
    vs = [m for m in cfg["matchups"] if not m.startswith("_")]
    print("Value per point, Stamina = 1.00.  Format: agi / int   (best of Sta/Agi/Int in brackets)\n")
    print(f"{'':10s}" + "".join(f"{b:>22s}" for b in builds))
    for m in vs:
        row = f"{m:10s}"
        for b in builds:
            w = stat_weights(Model(cfg, b, m), base)
            top = max(("sta", "agi", "int"), key=lambda k: w[k])
            row += f"{w['agi']:>9.2f} / {w['int']:.2f} [{top}]"
        print(row)
    print("\nOOM time (seconds) with base_gear.json:")
    for b in builds:
        d = Model(cfg, b, "generic").derived(base)
        print(f"  {b:14s} {d['oom_at']:.0f}s   ({cfg['builds'][b]['desc']})")


def cmd_weights(model, base):
    w = stat_weights(model, base)
    d = model.derived(base)
    print(f"At base gear: HP {d['hp']:.0f}  EHP {d['ehp']:.0f}  mana {d['mana']:.0f}  RAP {d['rap']:.0f}  "
          f"crit {d['crit']:.1f}%  DPS {d['dps']:.1f}  shot uptime {d['uptime']*100:.0f}% (OOM at {d['oom_at']:.0f}s)")
    print("\nValue per point (Stamina = 1.00):")
    for k, v in sorted(w.items(), key=lambda kv: -kv[1]):
        print(f"  {k:6s} {v:6.2f}")
    print("\nAs duel length changes (same opponent damage mix):")
    print("  duel_s  sta   agi   int   spi   mp5  | best of sta/agi/int")
    L0 = model.m["duel_sec"]
    cross = None
    for L in (20, 30, 45, 60, 75, 90, 120, 150, 180):
        model.m["duel_sec"] = L
        ww = stat_weights(model, base)
        top = max(("sta", "agi", "int"), key=lambda k: ww[k])
        print(f"  {L:5d}  {ww['sta']:.2f}  {ww['agi']:.2f}  {ww['int']:.2f}  {ww['spi']:.2f}  {ww['mp5']:.2f}  | {top}")
        if cross is None and ww["int"] > ww["agi"]:
            cross = L
    model.m["duel_sec"] = L0
    print(f"\nInt passes Agi once duels last about {cross}s or more." if cross
          else "\nAgi stays ahead of Int at every tested duel length.")


def cmd_slots(model, items, enchants, base, top):
    s0 = model.score(base)
    gain = lambda i: (model.score(add(base, i)) - s0) * 1000
    for s in SLOTS:
        rows = [i for i in items if i["slot"] in FITS[s] and i["has_stats"]]
        erows = [e for e in enchants if e["slot"] == s and e["has_stats"]]
        if not rows:
            continue
        print(f"\n== {s} ==")
        for i in sorted(rows, key=lambda i: -gain(i))[:top]:
            lvl = f"L{int(float(i['req_level']))}" if i.get("req_level") else ""
            print(f"  {gain(i):6.1f}  {i['name']:<40} {lvl:>4} {fmt_stats(i)}  [{i.get('source','')}]")
        for e in sorted(erows, key=lambda e: -gain(e))[:3]:
            print(f"   ench {gain(e):5.1f}  {e['name']:<35} {fmt_stats(e)}")
    print("\n(score = duel score gain x1000 when added on top of base_gear.json)")


def cmd_set(model, items, enchants, quiet=False):
    positions, chosen, ench, g = best_set(model, items, enchants)
    d = model.derived(g)
    if not quiet:
        print("\nOptimised set:")
        for k, s in enumerate(positions):
            it, e = chosen[k], ench[k]
            if not it:
                print(f"  {s:10s} -")
                continue
            extra = f"  + {e['name']}" if e else ""
            print(f"  {s:10s} {it['name']}{extra}  ({fmt_stats(it)})  {link(it)}")
        print(f"\nTotals from gear: {fmt_stats(g)}")
        print(f"HP {d['hp']:.0f}  EHP {d['ehp']:.0f}  mana {d['mana']:.0f}  RAP {d['rap']:.0f}  crit {d['crit']:.1f}%  "
              f"dodge {d['dodge']:.1f}%  DPS {d['dps']:.1f}  shot uptime {d['uptime']*100:.0f}%  "
              f"EHP x DPS {d['ehp']*d['dps']:.0f}")
    return d


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["matrix", "weights", "slots", "set", "compare", "all"])
    ap.add_argument("--build")
    ap.add_argument("--vs", help="matchup from config.json (priest, rogue, ...)")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--faction", choices=["any", "alliance", "horde"], help="override filters.faction")
    ap.add_argument("--duel", type=float, help="override the matchup's duel length (s)")
    ap.add_argument("--config", default=os.path.join(HERE, "config.json"))
    a = ap.parse_args()

    cfg = json.load(open(a.config))
    global ALLOW_DUPLICATES
    ALLOW_DUPLICATES = cfg.get("filters", {}).get("allow_duplicate_items", False)
    build = a.build or cfg["default_build"]
    vs = a.vs or cfg["default_matchup"]
    if a.duel:
        cfg["matchups"][vs]["duel_sec"] = a.duel
    if a.faction:
        cfg.setdefault("filters", {})["faction"] = a.faction
    items = load_rows(os.path.join(HERE, "items.csv"), cfg.get("filters", {}))
    items += load_rows(os.path.join(HERE, "items_manual.csv"), cfg.get("filters", {}))
    enchants = load_rows(os.path.join(HERE, "enchants.csv"))
    base = zero()
    bpath = os.path.join(HERE, "base_gear.json")
    if os.path.exists(bpath):
        base.update({k: float(v) for k, v in json.load(open(bpath)).items() if k in STATS})

    print(f"build: {build}   vs: {vs}   ({len(items)} items after filters)\n")
    model = Model(cfg, build, vs)
    if a.cmd in ("matrix", "all"):
        cmd_matrix(cfg, base)
    if a.cmd in ("weights", "all"):
        cmd_weights(model, base)
    if a.cmd in ("slots", "all"):
        cmd_slots(model, items, enchants, base, a.top)
    if a.cmd in ("set", "all"):
        cmd_set(model, items, enchants)
    if a.cmd == "compare":
        print("Each build with its own best set, against the same opponent:")
        for b in [b for b in cfg["builds"] if not b.startswith("_")]:
            d = cmd_set(Model(cfg, b, vs), items, enchants, quiet=True)
            print(f"  {b:14s} EHP {d['ehp']:6.0f}  DPS {d['dps']:5.1f}  EHP x DPS {d['ehp']*d['dps']:8.0f}  OOM {d['oom_at']:.0f}s")


if __name__ == "__main__":
    sys.exit(main())
