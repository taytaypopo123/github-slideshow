#!/usr/bin/env python3
"""Fetch stats for random-suffix item variants from Wowhead's XML tooltips.
Usage:
  python3 fetch_suffixes.py <scrape_dir> map    # one tooltip per suffix bonus ID -> tips_map.json
  python3 fetch_suffixes.py <scrape_dir> full   # every kept (item, suffix) pair -> tips_full.json
"""
import json, os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
D = sys.argv[1]; mode = sys.argv[2]
CACHE = os.path.join(D, "tips"); os.makedirs(CACHE, exist_ok=True)
STAT = {"Agility":"agi","Stamina":"sta","Intellect":"int","Spirit":"spi","Strength":"str"}
def tip(i, b):
    p = os.path.join(CACHE, f"{i}_{b}.xml")
    if not os.path.exists(p) or os.path.getsize(p) < 200:
        subprocess.run(["curl","-sSL","--retry","3","-A","Mozilla/5.0","-o",p,f"https://www.wowhead.com/forever/item={i}?bonus={b}&xml"])
    s = open(p, errors="ignore").read()
    n = re.search(r"<name><!\[CDATA\[(.*?)\]\]>", s)
    t = re.sub(r"<[^>]+>", " ", s.replace("<br>", "\n"))
    st = {STAT[k]: int(v) for v, k in re.findall(r"\+(\d+) (Agility|Stamina|Intellect|Spirit|Strength)", t)}
    for v in re.findall(r"Increases (?:ranged )?attack power by (\d+)", t): st["ap"] = st.get("ap", 0) + int(v)
    for v in re.findall(r"\+ ?(\d+) Attack Power", t): st["ap"] = st.get("ap", 0) + int(v)
    rest = [x.strip() for x in re.findall(r"Equip: ([^\n<]*?)(?:\s{2,}|$)", t)]
    return {"name": n.group(1) if n else None, "stats": st, "equip": rest}
pairs = json.load(open(os.path.join(D, "bonus_pairs.json")))
if mode == "map":
    jobs = [(v[len(v)//2][0], b) for b, v in pairs.items()]
else:
    keep = set(json.load(open(os.path.join(D, "keep_bonuses.json"))))
    items = {x["id"]: x for x in json.load(open(os.path.join(D, "items.json")))}
    jobs = [(i, b) for b, v in pairs.items() if int(b) in keep for i, l in v
            if i in items and items[i].get("quality", 0) >= 2 and (items[i].get("reqlevel") or 0) >= 18
            and items[i].get("_cat") != "armor/mail"]
print(len(jobs), "requests", file=sys.stderr)
with ThreadPoolExecutor(6) as ex:
    res = list(ex.map(lambda j: (j, tip(*j)), jobs))
out = {f"{i}_{b}": r for (i, b), r in res}
json.dump(out, open(os.path.join(D, f"tips_{mode}.json"), "w"))

if mode == "map":
    keep = [int(k.split("_")[1]) for k, v in out.items()
            if set(v["stats"]) & {"agi", "sta", "int"} or any("Attack Power" in e for e in v["equip"])]
    json.dump(keep, open(os.path.join(D, "keep_bonuses.json"), "w"))
