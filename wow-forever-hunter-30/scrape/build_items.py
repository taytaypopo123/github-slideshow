#!/usr/bin/env python3
"""Turn the Wowhead scrape (items.json + tips_full.json) into ../items.csv.

Run fetch_items.py and fetch_suffixes.py first (see README).
Usage: python3 build_items.py <scrape_dir>
"""
import csv
import json
import os
import re
import sys

D = sys.argv[1]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "items.csv")

# Forever tooltips: 14 crit rating = 1% crit, 10 hit rating = 1% hit
CRIT_RATING_PER_PCT = 14.0
HIT_RATING_PER_PCT = 10.0
HUNTER_CLASS_BIT = 1 << 2

SLOT = {1: "head", 2: "neck", 3: "shoulder", 16: "back", 5: "chest", 20: "chest", 9: "wrist",
        10: "hands", 6: "waist", 7: "legs", 8: "feet", 11: "finger", 12: "trinket",
        13: "one_hand", 21: "main_hand", 22: "off_hand", 17: "two_hand", 15: "ranged", 26: "ranged", 25: "ranged"}
SOURCE = {1: "crafted", 2: "drop", 3: "pvp", 4: "quest", 5: "vendor", 16: "world drop"}
ARMOR = {"armor/cloth": "cloth", "armor/leather": "leather", "armor/mail": "mail", "armor/cloaks": "cloth"}
COLS = ["name", "slot", "armor_type", "req_level", "item_level", "quality", "source", "agi", "sta", "int", "spi", "str",
        "ap", "rap", "mp5", "hit", "crit", "armor", "dps", "unique", "faction", "forever_status", "verified", "wowhead_id", "bonus", "notes"]


def base_row(x):
    e = x["jsonequip"]
    if e.get("classes") and not (e["classes"] & HUNTER_CLASS_BIT):
        return None
    slot = SLOT.get(x.get("slot") or e.get("slotbak"))
    if not slot:
        return None
    notes = []
    if e.get("reqfaction"):
        notes.append("reputation item")
    if e.get("itemset"):
        notes.append("set item")
    if e.get("cooldown"):
        notes.append("has on-use")
    if e.get("reqskill"):
        notes.append(f"needs profession skill {e.get('reqskillrank', '')} (skill id {e['reqskill']})")
    if (x.get("level") or 0) > 50 or x["name"].startswith("Monster -"):
        return None  # no-requirement endgame items, NPC-only weapons
    if (x.get("reqlevel") or e.get("reqlevel") or 0) <= 1 and (x.get("level") or 0) > 30:
        notes.append("no level req, high item level - check you can get it before 31")
    return {
        "name": x["name"], "slot": slot, "armor_type": ARMOR.get(x["_cat"], ""),
        "req_level": x.get("reqlevel") or e.get("reqlevel") or "", "item_level": x.get("level", ""),
        "quality": x.get("quality", ""),
        "source": "/".join(SOURCE.get(s, str(s)) for s in x.get("source", [])),
        "agi": e.get("agi", 0), "sta": e.get("sta", 0), "int": e.get("int", 0), "spi": e.get("spi", 0),
        "str": e.get("str", 0), "ap": e.get("atkpwr", 0), "rap": e.get("rgdatkpwr", 0), "mp5": e.get("manargn", 0),
        "hit": round(e.get("hitrtng", 0) / HIT_RATING_PER_PCT, 2),
        "crit": round(e.get("critstrkrtng", 0) / CRIT_RATING_PER_PCT, 2),
        "armor": (e.get("armor", 0) or 0) + (e.get("armorbonus", 0) or 0),
        "dps": e.get("rgddps", 0) if slot == "ranged" else 0,
        "unique": 1 if e.get("maxcount") == 1 else "",
        "faction": {1: "alliance", 2: "horde"}.get(x.get("side"), ""),
        "forever_status": (x.get("envChange") or {}).get("status", ""),
        "verified": "wowhead", "wowhead_id": x["id"], "bonus": "", "notes": "; ".join(notes),
    }


def main():
    items = json.load(open(os.path.join(D, "items.json")))
    tips_path = os.path.join(D, "tips_full.json")
    tips = json.load(open(tips_path)) if os.path.exists(tips_path) else {}
    by_id = {}
    for x in items:
        by_id.setdefault(x["id"], x)

    rows = []
    for x in by_id.values():
        r = base_row(x)
        if r:
            rows.append(r)
    seen = set()
    for key, t in tips.items():
        i, b = (int(v) for v in key.split("_"))
        x = by_id.get(i)
        if not x or not t.get("name"):
            continue
        r = base_row(x)
        if not r:
            continue
        r["name"], r["bonus"] = t["name"], b
        for s, v in t["stats"].items():
            r[s] = r.get(s, 0) + v
        sig = (i, r["name"], tuple(sorted(t["stats"].items())))
        if sig in seen:
            continue
        seen.add(sig)
        r["notes"] = "; ".join(filter(None, [r["notes"], "random suffix"]))
        rows.append(r)

    # Drop rows with nothing a hunter can use (pure spell power, spirit-only, etc.) except ranged weapons
    def useful(r):
        return r["slot"] == "ranged" or any(float(r[s] or 0) for s in ("agi", "sta", "int", "ap", "rap", "mp5", "hit", "crit"))
    rows = [r for r in rows if useful(r)]
    rows.sort(key=lambda r: (r["slot"], r["name"]))
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        for r in rows:
            w.writerow({c: ("" if r.get(c) in (0, 0.0, None) else r.get(c)) for c in COLS})
    print(f"wrote {len(rows)} rows to {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
