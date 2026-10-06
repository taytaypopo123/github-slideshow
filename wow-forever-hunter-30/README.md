# WoW Forever: Level 30 Hunter PvP Min-Max (duels)

A working file for finding the best duel gear for a level 30 Marksmanship hunter in WoW Forever. It has three parts:

- **This write-up**: how each stat turns into winning duels, and where Intellect passes Agility.
- **`items.csv` / `enchants.csv`**: the gear list. Add every candidate item from Wowhead's Forever database here.
- **`minmax.py`**: scores every item for your character, ranks each slot and picks the best full set.

```
python3 minmax.py weights          # value of each stat, and the Int vs Agi crossover
python3 minmax.py slots --top 10   # best items per slot
python3 minmax.py set              # best full set (one item + one enchant per slot)
python3 minmax.py all --duel 90    # everything, assuming 90-second duels
```

> **Status:** the item list is only a seed. These items and stats come from search-result snippets of community BiS sites (foreverchanges.pro, theforeverera.com, wowf.io). They are **not checked against Wowhead**, and some sources disagree. Every row is marked `verified=no` until someone checks it.

---

## The core idea: health × damage

A duel is a race. You win if you kill them before they kill you:

```
your effective HP / their DPS  >  their effective HP / your DPS
⇔  your EHP × your DPS  >  their EHP × their DPS
```

Their side is fixed, so you want to maximise **EHP × DPS**. Two consequences:

1. **1% more health is worth exactly 1% more damage.** Neither one is "the" stat. Whichever is cheaper to raise by 1% wins.
2. **Mana is damage over time.** While you have mana you cast Arcane, Serpent, Aimed and so on. Once you go OOM you only have Auto Shot. Mana only matters if the duel lasts longer than your mana does.

You said raw health and mana matter most to you. The model agrees about health, and agrees about mana once duels run past your OOM point.

## What each stat does at level 30 (Forever)

| Stat | What it gives a hunter | Duel value |
|---|---|---|
| **Stamina** | 10 HP per point | Always good. Direct EHP. |
| **Agility** | 1 ranged AP, crit (~1% per X agi at 30; measure it), 2 armor, a little dodge | Mostly damage, a bit of survival |
| **Intellect** | 15 mana. **With Careful Aim 5/5 it also gives 1 AP** (20% of Int per rank) | Damage like AP, plus mana if you'd otherwise go OOM |
| **Spirit** | Mana regen only outside the 5-second rule (Classic: Spirit/5 + 15 per 2s tick) | Close to zero. You are casting the whole duel. |
| **Mp5** | Regen that works while casting | Zero if you never go OOM. Strong if you do. |
| **AP / RAP** | 1:1 ranged attack power | Same as the AP part of Agi or Int |
| **Hit / Crit** | Forever merges melee/ranged/spell hit and crit | Each 1% is very strong; rare on low-level gear |

### Agility vs Intellect, point for point (with Careful Aim 5/5)

- **Damage:** 1 Agi = 1 AP + crit. 1 Int = 1 AP. **Agi wins on damage, always.** The gap is the crit portion.
- **Survival:** Agi gives a little armor and dodge (only against physical damage). Int gives none.
- **Mana:** Int gives 15 mana. That is worth **nothing** if you'd win or die before going OOM, and **a lot** once you would run dry.

So **Int passes Agi when your duels outlast your mana**. With the placeholder numbers in `config.json`, a hunter with ~1250 mana spending ~20 mana/sec goes OOM at about 62 seconds:

```
duel_s  sta   agi   int   spi   mp5  | winner
   45  1.00  0.50  0.36  0.00  0.00  | sta
   60  1.00  0.50  0.36  0.00  0.00  | sta
   75  1.00  0.50  1.46  0.06  1.13  | int
  120  1.00  0.49  1.23  0.07  1.44  | int
```

(Values are per point, with Stamina = 1.00.) Two things stand out:

- **Stamina is worth about 2× Agility** in a duel at these gear levels. That matches the old 29-twink rule that stamina is king.
- **Once you'd go OOM, Intellect is the best stat**, ahead of even Stamina. Each point of Int buys back shots. This is the Forever change at work: Careful Aim means Int isn't wasted in short fights either (it's still worth 0.36 as AP).

The switch is sharp because the model treats OOM as a cliff. In practice it's a little softer (you choose when to stop casting), but the shape holds. **Stamina is the safe default. Int is the best pick if you go OOM in your duels. Agi is the damage tiebreaker.**

### Spirit

Ignore it. You are inside the 5-second rule almost the whole duel, so Spirit regen barely ticks. It scores about 0.00–0.09 per point. Only take it as a free extra on an item you want for other stats.

### Lessons from Classic 29 twinks

- Stamina first, then the best ranged weapon you can get. Weapon DPS drives Auto Shot, which is the damage you keep after going OOM.
- Scope, cloak agility, chest stats/stamina, bracer stamina, gloves agility and boots stamina or Minor Speed are the standard enchants. **Minor Speed on boots** is usually right for PvP even though it adds no stats. Kiting is worth more than 5 Stamina.
- Engineering trinkets (net, recombobulator, grenades) beat stat trinkets in duels.

## Calibrating (do this first; it changes the answer)

`config.json` ships with **placeholders**. The crossover depends almost entirely on your real mana pool and mana spend. On your level 30 hunter:

1. **Naked numbers**: take off all gear, read HP, mana, ranged AP, Agi/Sta/Int/Spi. Fill in `naked_*`, then set `base_hp = HP − 10×Sta`, `base_mana = mana − 15×Int`, `base_rap = RAP − Agi − Int` (with Careful Aim 5/5).
2. **Agi per 1% crit**: note crit %, put on a known +Agi item, and divide the Agi change by the crit change. Do the same for dodge.
3. **Careful Aim**: add some Int and check that **ranged** AP goes up. The tooltip says "Attack Power". If only melee AP moves, set `careful_aim_ranks` to 0.
4. **Mana spend**: duel a friend or a target dummy with your normal rotation. Divide mana spent by time to get `shot_mana_per_sec`. Note when you go OOM.
5. **Duel length**: set `duel_length_sec` to how long your duels actually last.
6. Put your current gear totals in `base_gear.json`.

## Updating the item list

Each row in `items.csv` is one item. Slots are: `head neck shoulder back chest wrist hands waist legs feet finger trinket main_hand off_hand two_hand ranged`. Leave blank any stat the item doesn't have. For ranged weapons, put the weapon DPS in `dps`. Mark `unique=1` for unique rings or trinkets. Set `verified=yes` once you've checked it on Wowhead. `--verified-only` then ignores the rest.

To cover all items, use Wowhead Forever's item search for each slot, filtered to required level ≤ 30, with any of Agility, Stamina, Intellect or Attack Power. Paste the results into the CSV. Include cloth, leather and mail: a cloth Int/Stam piece can beat a mail Agi piece in this model.

## Talents at level 30 (21 points)

- Commonly listed MM PvP build: **0/21/0**. It includes Careful Aim 5/5 (5-point tier), Lethal Attacks, Mortal Shots 5/5, Hawk Eye 3/3, Rapid Killing 2/2 and Trueshot Aura.
- **Lone Wolf** (10-point MM tier, 1 rank): +20% damage with no active pet. That's a large damage boost, but it costs your pet as a second damage source and peel. Not modelled here.
- Check whether any tree has a **% health** talent within reach. If you take one, put it in `hp_mult`.

## Sources

- [Wowhead – Hunter talent changes (Forever)](https://www.wowhead.com/forever/changes/talents/hunter) · [Talent calculator](https://www.wowhead.com/forever/talent-calc/hunter)
- [Icy Veins – New hunter abilities (Careful Aim)](https://www.icy-veins.com/wow-forever/news/new-abilities-for-hunter-mage-and-paladin-in-wow-forever/) · [Icy Veins – MM guide](https://www.icy-veins.com/wow-forever/marksmanship-hunter-ranged-dps-pve-guide)
- [Warcraft Tavern – Forever hunter guide](https://www.warcrafttavern.com/forever/guides/hunter/) · [Warcraft Tavern – Classic 29 twink hunter](https://www.warcrafttavern.com/wow-classic/guides/29-twink-hunter/)
- [ForeverChanges – Hunter PvP BiS (L30)](https://foreverchanges.pro/bis/hunter/pvp) · [The Forever Era – MM BiS L30](https://theforeverera.com/en/bis/hunter/marksmanship/30/) · [WOWF.IO – Hunter BiS](https://wowf.io/en/bis/hunter)
- [Icy Veins – Forever itemization rework](https://www.icy-veins.com/wow-forever/news/wow-forever-is-completely-reworking-classic-itemization/) · [Icy Veins – Forever PvP overview](https://www.icy-veins.com/wow-forever/pvp-overview)
