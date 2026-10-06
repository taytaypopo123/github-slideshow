# WoW Forever: Level 30 Hunter PvP Min-Max (duels)

Finds the best duel gear for a level 30 hunter in WoW Forever by scoring **every** item a hunter can use, for different talent builds and opponents.

- **`items.csv`**: 5,779 items pulled from Wowhead's Forever database. It covers cloth, leather, cloaks, rings, necks, trinkets, bows, guns, crossbows and melee weapons with required level 10–30 (plus low-level items with no requirement), including every random-suffix version with Agi, Sta, Int or AP ("of the Eagle", "of the Monkey", "of the Bandit" and so on). Each row has a Wowhead link (`wowhead_id` + `bonus`).
- **`items_manual.csv`**: hand-added items, starting with Engineering gear (no level requirement) that Wowhead's lists miss. Add your own finds here; a re-scrape won't overwrite it.
- **`enchants.csv`**: Forever's enchanting recipes with Agi, Sta, Int, stats or regen, values taken from Wowhead.
- **`minmax.py`**: scores items, ranks each slot, builds the best full set and compares talent builds.
- **`config.json`**: your character, the talent builds and the matchups. Several numbers are **placeholders** (see Calibrating).
- **`priest_duel.py` / `priest_duel.json`**: second-by-second hunter vs priest simulator (mana war, Penance, Dismember).
- **`RESULTS.md`**: current output (stat values, best sets, build comparison).
- **`scrape/`**: scripts to re-download the item data when Wowhead updates.

```
python3 minmax.py matrix                                  # Sta/Agi/Int value for every build x opponent
python3 minmax.py compare --vs priest --faction horde     # which talent build wins vs a priest
python3 minmax.py set --build sv_mm_tank --vs rogue --faction alliance
python3 minmax.py slots --build mm_pet --vs generic --top 10
python3 minmax.py weights --build bm --vs priest
```

---

## How it scores

A duel is a race: you win if `your EHP × your DPS > their EHP × their DPS`. Their side is fixed, so the tool maximises **EHP × DPS**:

- **1% more health is worth exactly 1% more damage.** Neither one is "the" stat.
- **Mana is damage over time.** Shots run until you go OOM. After that you only have Auto Shot and your pet. Int and Mp5 are worth almost nothing until a duel lasts longer than your mana, then they jump.
- EHP includes armor and dodge, scaled by how much of the opponent's damage is physical.

## What we found

### Stats (Forever, level 30)

| Stat | What it does | Duel value |
|---|---|---|
| **Stamina** | 10 HP. Survivalist adds +10% to the total | The default best stat. Roughly 2× Agi in most matchups |
| **Agility** | 1 ranged AP, crit, 2 armor, a little dodge | Damage first. Best in short physical fights (rogue, warrior, hunter) |
| **Intellect** | 15 mana. **With Careful Aim 5/5 also 1 AP** | 0.3× Sta while you have mana. **Overtakes Sta once you'd go OOM** |
| **Spirit** | Regen only outside the 5-second rule | About 0. Ignore it. |
| **Mp5** | Regen while casting | 0 in short duels, strong in long ones |

**When does Int beat Agi?** Only when the duel outlasts your mana. With the placeholder numbers that's priests (~120s), paladins and druids, where Int comes out as the best stat of all. In short duels (rogue, warrior, mage) Stamina wins and Int counts only as attack power. You were right that this mostly comes down to priests and other long fights. Watching priest duels to get real `duel_sec` and mana-spend numbers is the best next step.

**With BM** (no Careful Aim), Int is only mana. It drops to 0 in short duels and never passes Stamina.

### Forever-specific findings from Wowhead

- **Survivalist (SV tier 2) is now "+10% total Health"** (5 ranks). With 10 points in SV (Improved Tracking 5 + Survivalist 5) you still have 11 for MM: Lethal Attacks 5, **Careful Aim 5**, plus 1. That's the `sv_mm_tank` build. It comes out on top in every matchup tested.
- **Careful Aim** (MM tier 2): "Increases your Attack Power by 20% of your Intellect" per rank, 100% at 5/5.
- **Lone Wolf** (MM tier 3): +20% damage with no pet. In the model it's second best overall and the best pure-damage build.
- **Thick Hide is removed.** Lightning Reflexes (+15% Agi) is SV tier 6, out of reach at 21 points.
- **Random suffixes favor Sta and Int.** At the same item level "of Stamina" and "of Intellect" give about 2× the points of "of Agility" (e.g. +8 Sta or +8 Int vs +4 Agi). "of the Eagle" (Sta/Int) gives 5/5 where "of the Monkey" (Agi/Sta) gives 3/3. For a Sta/Int plan, Eagle and Stamina suffixes are very efficient.
- **Mail starts at 40.** Forever's hunter change list doesn't touch it, so mail is filtered out (`filters.allow_mail`). Some "Chain" items are leather in Forever, though: **Highlander's (Alliance) and Defiler's (Horde) Chain Girdle are leather** and allowed.
- **Rating conversions** from tooltips: 14 crit rating = 1% crit, 10 hit rating = 1% hit.
- **Necklace enchant exists** (Necklace – Agility, +5). There are also large melee-weapon stat enchants (Weapon – Agility +15, Weapon – Mighty Intellect +22, 2H – Agility +25). Hunters get the stats from whatever melee weapon they hold. **I couldn't confirm whether Forever lets these high-level enchants go on level 30 gear.** Check in game, and delete rows from `enchants.csv` that aren't possible.
- Mana costs are a % of base mana (e.g. Multi-Shot "13% of base power"), so extra Int raises your pool without raising costs.

### Builds in config.json (21 points)

| Build | Key talents | Model result (placeholder numbers) |
|---|---|---|
| `sv_mm_tank` | Improved Tracking 5, Survivalist 5 / Lethal Attacks 5, Careful Aim 5 | Best EHP × DPS in every matchup tested (generic, priest, rogue) |
| `mm_lone_wolf` | Lethal 5, Careful Aim 5, Efficiency 4, Lone Wolf, Mortal Shots 5, Trueshot | Highest DPS, 2nd overall |
| `mm_pet` | Same with pet, Efficiency 5 | 3rd |
| `bm` | Focused Fire, Unleashed Fury, Ferocity, Hawk, Intimidation | Last, **but** the model only counts pet damage, not Intimidation's stun or pet peel/interrupts |

The model doesn't value crowd control at all: Scatter Shot, Freezing Trap, Intimidation, Concussive procs, kiting. Use it to compare gear within a build, and treat the build comparison as a rough guide.

### Best sets

See **RESULTS.md**. One thing stands out: the best duel set changes surprisingly little between opponents. Brawler's Leather Helm, Ghostshard Talisman, Truthseeker's Bow, Wyvern Heart Band, the PvP-rep trinkets and Stamina/Bandit suffixes show up everywhere. Against priests it swaps in Int pieces: Defiler's Mail Girdle (+5 Sta +12 Int, also leather despite the name), Necromancer Leggings and Int enchants.

## Twink tips: classic 29-twink wisdom, checked against Forever

Classic 29-twink guides (Warcraft Tavern, OwnedCore, xpoff) agree on a few things: **Stamina first, then the best bow or gun you can get, then Agility**. **Engineering is mandatory.** Carry a full bag of consumables. In 1v1, a Survival-leaning build with Surefooted, Deterrence and Improved Wing Clip was preferred against rogues. Here's how those hold up in Forever at 30, checked on Wowhead:

**What's different in Forever (changes classic advice)**
- **No Viper Sting at 30**, so you can't drain a priest's mana. The mana fight is about your own pool. Classic guides' "Viper the priest" doesn't apply.
- **Traps are on a 30s cooldown** (Freezing, Frost, Immolation; was 15s). Trap-kiting is weaker, so make each Freezing Trap count.
- **Feign Death at 30** (80 mana, 30s CD). This is why 30 is stronger for hunters than classic 29: drop combat, reset, re-trap.
- **Scatter Shot is MM tier 5 (20 points).** The Survivalist hybrid (`sv_mm_tank`) **can't reach it**; full MM can. That's the biggest cost of the hybrid, and the model doesn't count it.
- **Multi-Shot now has a 0.5s cast and 6s CD; Aimed Shot is a 2s cast** sharing that CD. Arcane Shot and Serpent Sting cost 80 mana, Aimed 115. With ~1,200–1,500 mana that's roughly 15 shots, so mana really does run out in long duels.
- **Aspect of the Monkey = 8% dodge.** Use it in melee range against rogues and warriors.
- **New pet abilities** (Wowhead lists them on the hunter page; check which family has which): **Dismember** (-50% healing for 10s, strong against priests, paladins and druids), **Mine!** (4s disarm, against warriors and rogues), **Web** (root), **Pinch** and **Tendon Rip** (50% snare), **Savage Rend** (bleed). These are likely a bigger deal for duels than the classic boar-charge advice.
- **Discolored Healing Potions** are new: Greater Discolored (req 21) heals **975–1105 instantly**, then you take 75% of that back over time as a poison or disease. The plain Greater Healing Potion is 455–585. That's a big burst heal to win a race with.
- **Lesser Mageblood Elixir** (req 25): 6 mana per 5 sec for 30 min. Mp5 that works while casting, good for priest duels.
- **PvP bandages** (Defiler's, Highlander's, Arathi Basin, Darkspear Islands Silk Bandage: 640 over 8s) only work inside their battleground. In duels use **Heavy Silk Bandage** (also 640, First Aid 125).
- **Scopes at 30:** Deadly Scope (+5 damage) needs level 30. The +3% hit (Biznicks) and +2% crit (SAF-T) scopes need 50–60, so they're out.

**Engineering at 30.** None of these have a level requirement, only Engineering skill:
- *Gear:* **Goblin Rocket Helmet** (+15 Sta, Eng 235; on-use charge that incapacitates for 30s, broken by damage), **Gnomish Goggles** (+9 Agi/Sta/Spi, Eng 210), **Gnomish Harm Prevention Belt** (leather, +6 Sta, **500-damage shield** on use, Eng 215), **Parachute Cloak** (+8 Agi, Eng 225), **Goblin Rocket Boots** (speed burst, **no Engineering needed** to wear).
- *Trinkets:* **Gnomish Net-o-Matic** (10s net, Eng 210), **Goblin Mortar** (393–531 damage + 3s stun, Eng 205), **Gnomish Shrink Ray** (-250 attack power, wrecks warriors and rogues, Eng 205), **Goblin Bomb Dispenser** (315–385, Eng 230), **Minor Recombobulator** (heal and mana), **Gnomish Cloaking Device**, **Gnomish Battle Chicken**.
- *Throwables:* **Iron Grenade** (132–218 + 3s stun, Eng 175). Explosive Sheep (150), Goblin Land Mine (450, Eng 195), Large Copper Bomb (1s stun). Non-engineers get EZ-Thro/SAF-T dynamite, and SAF-T Jumbo Dynamite (128–172) lists no requirements, so check it in game.
- The on-use effects aren't in the stat model. The engineering gear is in `items_manual.csv`; pick trinkets by hand. Two on-use trinkets usually beat any +6 Sta trinket.

**Consumables available at 30 (Wowhead Forever):**

| Item | Effect | Req |
|---|---|---|
| Elixir of Agility | +15 Agi, 1h | 27 |
| Elixir of Defense | +250 armor | 29 |
| Elixir of Wisdom | +6 Int | 10 |
| Lesser Mageblood Elixir | 6 mp5, 30 min | 25 |
| Scroll of Stamina II / Agility II / Protection III | +8 Sta / +9 Agi / +180 armor | 20/25/30 |
| Greater Discolored Healing Potion | 975–1105 instant, then 75% back over time | 21 |
| Greater Healing Potion | 455–585 | 21 |
| Mana Potion | 455–585 mana | 22 |
| Free Action Potion | 30s stun/snare immunity (against rogues and warriors) | 20 |
| Swiftness Potion | +50% run speed, 15s | 5 |
| Heavy Silk Bandage | 640 over 8s | First Aid 125 |

Not available at 30: Elixir of Fortitude (now 45), Restorative Potion (32), Living Action (47), Limited Invulnerability (45).

**Professions:** Engineering plus a second one. Enchanting (if Forever lets these go on level 30 gear: Superior Stamina bracer, Major Stamina chest, +5 Agi necklace, +15 Agi or +22 Int weapon), First Aid always. Classic advice was Engineering plus Enchanting or Alchemy.

## Priest duels: `priest_duel.py`

`minmax.py` doesn't model the priest's healing, so priest duels have their own simulator. It tracks both health and mana bars every second. The priest heals with Forever's level-30 spells: **Penance** (baseline, 3×184 for 100 mana on a 12s cooldown, ~5.5 HP per mana), Power Word: Shield, Heal, Flash Heal, Desperate Prayer and a potion. It also uses Inner Fire, and Mana Burn if enabled. It compares four hunter strategies:

```
python3 priest_duel.py                                   # compare strategies
python3 priest_duel.py --trace spam                      # second-by-second log
python3 priest_duel.py --set priest.mana=2200 --set priest.mana_burn=true
```

What it shows with the placeholder numbers (edit `priest_duel.json` after watching real duels):
- **Penance covers your first ~46 DPS almost for free**, so free damage alone (Auto Shot + pet) only drains a priest slowly.
- **Your pet decides it.** Without a pet and Dismember (−50% healing for 10s), the hunter loses every scenario against a well-geared priest. With them, the hunter wins most. **Don't play Lone Wolf against priests.**
- **Spend your mana. Don't hoard it.** Spamming shots or bursting won more often than saving mana. Against a tanky, high-mana priest, every strategy that held mana back died with mana unspent. Against Mana Burn, mana you don't spend gets burned anyway.
- Unconfirmed: Dismember's cooldown and Forever's Weakened Soul duration. Both are placeholders.

## Calibrating (do this; it changes the answers)

`config.json` ships with placeholders. On your level 30 hunter:

1. **Naked numbers** with no HP talents: HP, mana, ranged AP, Agi/Sta/Int/Spi. Set `base_hp = HP − 10×Sta`, `base_mana = mana − 15×Int`, `base_rap = RAP − Agi − Int` (with Careful Aim 5/5).
2. **Agi per 1% crit**: note crit %, put on a known +Agi item, and divide the Agi change by the crit change. Do the same for dodge.
3. **Careful Aim check**: add Int and confirm **ranged** AP rises.
4. **Rotation**: duel a dummy or a friend for 30s. `shot_mana_per_sec` = mana spent ÷ 30. `shot_dps` = extra damage from shots beyond Auto Shot ÷ 30. `pet_dps` = pet damage ÷ 30.
5. **Matchups**: from duels you play or watch, set each class's `duel_sec` and `physical_frac`.
6. **`base_gear.json`**: your current gear totals. Stat values are measured on top of these.
7. **`filters.faction`**: `horde` or `alliance` (or pass `--faction`).

## Updating the item data

```
cd wow-forever-hunter-30/scrape
python3 fetch_items.py /tmp/wh            # item lists (cached in /tmp/wh/raw)
python3 fetch_suffixes.py /tmp/wh map     # one tooltip per suffix type
python3 fetch_suffixes.py /tmp/wh full    # every relevant suffixed item (~5,700 tooltips, ~3 min)
python3 build_items.py /tmp/wh            # rewrites ../items.csv
```

This needs `www.wowhead.com` to be reachable. Suffix variants are fetched for green-or-better, required level 18+, non-mail items. `items.csv` can also be edited by hand: add a row, and leave stats blank if the item doesn't have them. Gaps to know about:
- On-use trinkets (Engineering gadgets etc.) have no stats, so they never score. Pick those by hand.
- Set bonuses aren't counted.
- Items Wowhead marks `unconfirmed` (see `forever_status`) may change.
- `filters.allow_duplicate_items` is off, so the same ring, trinket or weapon is never used twice.

## Sources

- Wowhead Forever: [item database](https://www.wowhead.com/forever/items), [hunter talent changes](https://www.wowhead.com/forever/changes/talents/hunter), [hunter spellbook changes](https://www.wowhead.com/forever/changes/spellbook/hunter), [enchanting](https://www.wowhead.com/forever/spells/professions/enchanting)
- [Icy Veins – New hunter abilities](https://www.icy-veins.com/wow-forever/news/new-abilities-for-hunter-mage-and-paladin-in-wow-forever/) · [Icy Veins – Forever itemization rework](https://www.icy-veins.com/wow-forever/news/wow-forever-is-completely-reworking-classic-itemization/) · [Icy Veins – Forever PvP overview](https://www.icy-veins.com/wow-forever/pvp-overview)
- [Warcraft Tavern – Classic 29 twink hunter](https://www.warcrafttavern.com/wow-classic/guides/29-twink-hunter/) (historical stat priorities)
- Community BiS lists for comparison: [ForeverChanges](https://foreverchanges.pro/bis/hunter/pvp), [The Forever Era](https://theforeverera.com/en/bis/hunter/marksmanship/30/)
