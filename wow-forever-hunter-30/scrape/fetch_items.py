#!/usr/bin/env python3
"""Download every hunter-usable WoW Forever item with required level 10-30 from Wowhead's item lists.
Usage: python3 fetch_items.py <scrape_dir>      (writes <scrape_dir>/items.json and bonus_pairs.json)
Pages are cached in <scrape_dir>/raw, so re-runs only fetch what's missing.
"""
import json, os, re, subprocess, sys, time
OUT = sys.argv[1]; os.makedirs(os.path.join(OUT, "raw"), exist_ok=True)
CATS = ["armor/cloth","armor/leather","armor/mail","armor/amulets","armor/rings","armor/trinkets","armor/cloaks",
        "weapons/bows","weapons/guns","weapons/crossbows","weapons/one-handed-axes","weapons/one-handed-swords",
        "weapons/daggers","weapons/fist-weapons","weapons/two-handed-axes","weapons/two-handed-swords",
        "weapons/polearms","weapons/staves"]
RANGES = [(10,30)]
def get(url):
    p = os.path.join(OUT, "raw", re.sub(r"[^a-z0-9]+","_",url)+".html")
    if not os.path.exists(p):
        subprocess.run(["curl","-sS","-A","Mozilla/5.0","-o",p,url],check=True); time.sleep(0.7)
    return open(p).read()
def parse(s):
    eq = {}
    for m in re.finditer(r"WH\.Gatherer\.addData\(3,\s*\d+,\s*(\{.*?\})\);", s, re.S):
        try:
            for k,v in json.loads(m.group(1)).items(): eq[int(k)] = v
        except Exception as e: print("addData parse fail", e, file=sys.stderr)
    m = re.search(r"var listviewitems = (\[.*?\]);\s*\n", s, re.S)
    lv = []
    if m:
        txt = re.sub(r"(\{|,)\s*([A-Za-z_]\w*)\s*:", r'\1"\2":', m.group(1))
        lv = json.loads(txt)
    found = re.search(r"([\d,]+) items found", s)
    return eq, lv, (found.group(1) if found else "?")
items = {}
def run(cat, lo, hi, depth=0):
    url = f"https://www.wowhead.com/forever/items/{cat}/min-req-level:{lo}/max-req-level:{hi}"
    eq, lv, found = parse(get(url))
    n = int(found.replace(",","")) if found != "?" else len(lv)
    print(f"{cat} {lo}-{hi}: found {found}, got {len(lv)}", file=sys.stderr)
    if n > len(lv) and hi > lo:
        mid = (lo+hi)//2; run(cat, lo, mid, depth+1); run(cat, mid+1, hi, depth+1); return
    for it in lv:
        e = eq.get(it["id"], {})
        it["jsonequip"] = e.get("jsonequip", {}); it["attainable"] = e.get("attainable")
        it["_cat"] = cat
        items[it["id"]] = it
for c in CATS:
    for lo,hi in RANGES: run(c, lo, hi)
json.dump(list(items.values()), open(os.path.join(OUT,"items.json"),"w"))
print(len(items), "items", file=sys.stderr)

# random-suffix variants ("of the Eagle" etc.) are listed as bonus IDs; record them for fetch_suffixes.py
import collections
pairs = collections.defaultdict(set)
for p in os.listdir(os.path.join(OUT, "raw")):
    _, lv, _ = parse(open(os.path.join(OUT, "raw", p)).read())
    for x in lv:
        for b in x.get("bonuses", []):
            pairs[b].add((x["id"], x.get("level")))
json.dump({str(b): sorted(v) for b, v in pairs.items()}, open(os.path.join(OUT, "bonus_pairs.json"), "w"))
