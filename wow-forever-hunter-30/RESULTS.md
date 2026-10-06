# Generated results

Output of `minmax.py` using the **placeholder** numbers in config.json, so rerun after calibrating. Item data from Wowhead's Forever database, 2026-10-06. Links open the exact item (including its random suffix).

## `python3 minmax.py matrix`

```
build: mm_pet   vs: generic   (5387 items after filters)

Value per point, Stamina = 1.00.  Format: agi / int   (best of Sta/Agi/Int in brackets)

                    mm_lone_wolf                mm_pet            sv_mm_tank                    bm
generic        0.50 / 0.36 [sta]     0.44 / 0.31 [sta]     0.43 / 0.32 [sta]     0.44 / 0.00 [sta]
priest         0.42 / 1.29 [int]     0.35 / 1.10 [int]     0.34 / 1.05 [int]     0.34 / 0.65 [sta]
paladin        0.53 / 1.38 [int]     0.47 / 1.19 [int]     0.45 / 1.13 [int]     0.45 / 0.72 [sta]
druid          0.48 / 1.48 [int]     0.42 / 1.03 [int]     0.41 / 1.25 [int]     0.41 / 0.82 [sta]
shaman         0.48 / 0.36 [sta]     0.43 / 0.31 [sta]     0.42 / 0.32 [sta]     0.43 / 0.00 [sta]
warlock        0.43 / 0.90 [sta]     0.38 / 0.48 [sta]     0.36 / 1.28 [int]     0.37 / 0.85 [sta]
hunter         0.54 / 0.36 [sta]     0.49 / 0.31 [sta]     0.48 / 0.32 [sta]     0.49 / 0.00 [sta]
mage           0.43 / 0.36 [sta]     0.37 / 0.31 [sta]     0.36 / 0.32 [sta]     0.38 / 0.00 [sta]
warrior        0.55 / 0.36 [sta]     0.50 / 0.31 [sta]     0.49 / 0.32 [sta]     0.50 / 0.00 [sta]
rogue          0.55 / 0.36 [sta]     0.50 / 0.31 [sta]     0.49 / 0.32 [sta]     0.50 / 0.00 [sta]

OOM time (seconds) with base_gear.json:
  mm_lone_wolf   71s   (0/21/0: Lethal Attacks 5, Careful Aim 5, Efficiency 4, Lone Wolf 1, Mortal Shots 5, Trueshot Aura 1 - no pet)
  mm_pet         73s   (0/21/0 with a pet: Lethal Attacks 5, Careful Aim 5, Efficiency 5, Mortal Shots 5, Trueshot Aura 1)
  sv_mm_tank     64s   (0/11/10: Improved Tracking 5, Survivalist 5 / Lethal Attacks 5, Careful Aim 5, Efficiency 1 - +10% HP, keeps Careful Aim)
  bm             62s   (21/0/0: Deadly Aspects/Endurance Training, Focused Fire 2, Unleashed Fury 5, Ferocity 5, Summon Hawk, Spirit Bond, Intimidation - no Careful Aim)
```

## `python3 minmax.py compare --vs generic --faction horde`

```
build: mm_pet   vs: generic   (5188 items after filters)

Each build with its own best set, against the same opponent:
  mm_lone_wolf   EHP   2892  DPS 167.2  EHP x DPS   483440  OOM 78s
  mm_pet         EHP   2989  DPS 149.3  EHP x DPS   446228  OOM 73s
  sv_mm_tank     EHP   3266  DPS 153.4  EHP x DPS   501112  OOM 81s
  bm             EHP   2950  DPS 137.2  EHP x DPS   404549  OOM 59s
```

## `python3 minmax.py compare --vs priest --faction horde`

```
build: mm_pet   vs: priest   (5188 items after filters)

Each build with its own best set, against the same opponent:
  mm_lone_wolf   EHP   2389  DPS 164.6  EHP x DPS   393282  OOM 120s
  mm_pet         EHP   2509  DPS 147.3  EHP x DPS   369547  OOM 121s
  sv_mm_tank     EHP   2772  DPS 147.3  EHP x DPS   408148  OOM 120s
  bm             EHP   2471  DPS 123.4  EHP x DPS   304821  OOM 116s
```

## `python3 minmax.py compare --vs rogue --faction horde`

```
build: mm_pet   vs: rogue   (5188 items after filters)

Each build with its own best set, against the same opponent:
  mm_lone_wolf   EHP   3335  DPS 166.6  EHP x DPS   555608  OOM 52s
  mm_pet         EHP   3431  DPS 149.8  EHP x DPS   513868  OOM 54s
  sv_mm_tank     EHP   3774  DPS 152.3  EHP x DPS   574819  OOM 47s
  bm             EHP   3442  DPS 145.0  EHP x DPS   499030  OOM 39s
```

## `python3 minmax.py set --build sv_mm_tank --vs generic --faction horde`

```
build: sv_mm_tank   vs: generic   (5188 items after filters)


Optimised set:
  head       Brawler's Leather Helm  (+10 agi, +13 sta, +84 armor)  https://www.wowhead.com/forever/item=252512
  neck       Ghostshard Talisman  + Necklace - Agility  (+9 sta, +14 ap)  https://www.wowhead.com/forever/item=7731
  shoulder   Pathfinder Shoulder Pads of the Bandit  (+3 agi, +7 sta, +7 ap, +71 armor)  https://www.wowhead.com/forever/item=15345?bonus=12751
  back       Tigerstrike Mantle  + Cloak - Minor Agility  (+8 agi, +7 sta, +25 armor)  https://www.wowhead.com/forever/item=13108
  chest      Raptor Hunter Tunic  + Chest - Major Stamina  (+3 agi, +16 sta, +4 str, +117 armor)  https://www.wowhead.com/forever/item=4119
  wrist      Unearthed Bands of Stamina  + Bracer - Superior Stamina  (+9 sta, +16 ap, +49 armor)  https://www.wowhead.com/forever/item=9428?bonus=13020
  hands      Razzeric's Racing Grips  + Gloves - Greater Agility  (+8 agi, +9 sta, +70 armor)  https://www.wowhead.com/forever/item=6727
  waist      Defiler's Leather Girdle  (+4 sta, +24 ap, +91 armor)  https://www.wowhead.com/forever/item=20191
  legs       Panther Hunter Leggings  + Armor Kit - Medium/Heavy (+24/+32 armor)  (+10 agi, +11 sta, +96 armor)  https://www.wowhead.com/forever/item=4108
  feet       Enchanted Sandals  + Boots - Greater Stamina  (+5 agi, +10 sta, +8 int, +36 armor)  https://www.wowhead.com/forever/item=279843
  finger     Wyvern Heart Band  (+5 agi, +5 sta, +15 ap)  https://www.wowhead.com/forever/item=285190
  finger     Determined Band  (+8 sta, +9 ap)  https://www.wowhead.com/forever/item=277208
  trinket    Defiler's Talisman  (+6 sta)  https://www.wowhead.com/forever/item=21120
  trinket    Rune of Duty  (+4 sta)  https://www.wowhead.com/forever/item=21568
  main_hand  Blade of the Magram Clan  + Weapon - Mighty Intellect  (+4 sta, +10 ap)  https://www.wowhead.com/forever/item=271796
  off_hand   Scout's Blade  + Weapon - Mighty Intellect  (+7 agi, +3 sta)  https://www.wowhead.com/forever/item=19545
  two_hand   -
  ranged     Truthseeker's Bow  + Deadly Scope (+5 dmg)  (+7 agi, +3 sta, +23.75 dps)  https://www.wowhead.com/forever/item=277254

Totals from gear: +84 agi, +154 sta, +52 int, +4 str, +95 ap, +671 armor, +25.54 dps
HP 2739  EHP 3266  mana 1570  RAP 346  crit 9.1%  dodge 4.1%  DPS 153.4  shot uptime 100%  EHP x DPS 501112
```

## `python3 minmax.py set --build sv_mm_tank --vs generic --faction alliance`

```
build: sv_mm_tank   vs: generic   (5228 items after filters)


Optimised set:
  head       Brawler's Leather Helm  (+10 agi, +13 sta, +84 armor)  https://www.wowhead.com/forever/item=252512
  neck       Ghostshard Talisman  + Necklace - Agility  (+9 sta, +14 ap)  https://www.wowhead.com/forever/item=7731
  shoulder   Pathfinder Shoulder Pads of the Bandit  (+3 agi, +7 sta, +7 ap, +71 armor)  https://www.wowhead.com/forever/item=15345?bonus=12751
  back       Mourning Shawl  + Cloak - Minor Agility  (+12 sta, +24 armor)  https://www.wowhead.com/forever/item=6751
  chest      Raptor Hunter Tunic  + Chest - Major Stamina  (+3 agi, +16 sta, +4 str, +117 armor)  https://www.wowhead.com/forever/item=4119
  wrist      Unearthed Bands of Stamina  + Bracer - Superior Stamina  (+9 sta, +16 ap, +49 armor)  https://www.wowhead.com/forever/item=9428?bonus=13020
  hands      Runebound Gloves  + Gloves - Greater Agility  (+10 sta, +5 spi, +16 ap, +71 armor)  https://www.wowhead.com/forever/item=279849
  waist      Highlander's Leather Girdle  (+4 sta, +24 ap, +91 armor)  https://www.wowhead.com/forever/item=20117
  legs       Panther Hunter Leggings  + Armor Kit - Medium/Heavy (+24/+32 armor)  (+10 agi, +11 sta, +96 armor)  https://www.wowhead.com/forever/item=4108
  feet       Highlander's Lizardhide Boots  + Boots - Greater Stamina  (+5 agi, +8 sta, +4 int, +104 armor)  https://www.wowhead.com/forever/item=20102
  finger     Wyvern Heart Band  (+5 agi, +5 sta, +15 ap)  https://www.wowhead.com/forever/item=285190
  finger     Determined Band  (+8 sta, +9 ap)  https://www.wowhead.com/forever/item=277208
  trinket    Talisman of Arathor  (+6 sta)  https://www.wowhead.com/forever/item=21119
  trinket    Rune of Duty  (+4 sta)  https://www.wowhead.com/forever/item=21568
  main_hand  Blade of the Magram Clan  + Weapon - Mighty Intellect  (+4 sta, +10 ap)  https://www.wowhead.com/forever/item=271796
  off_hand   Sentinel's Blade  + Weapon - Mighty Intellect  (+7 agi, +3 sta)  https://www.wowhead.com/forever/item=19549
  two_hand   -
  ranged     Truthseeker's Bow  + Deadly Scope (+5 dmg)  (+7 agi, +3 sta, +23.75 dps)  https://www.wowhead.com/forever/item=277254

Totals from gear: +68 agi, +158 sta, +48 int, +5 spi, +4 str, +111 ap, +739 armor, +25.54 dps
HP 2783  EHP 3325  mana 1513  RAP 342  crit 8.6%  dodge 3.6%  DPS 151.8  shot uptime 100%  EHP x DPS 504712
```

## `python3 minmax.py set --build sv_mm_tank --vs priest --faction horde`

```
build: sv_mm_tank   vs: priest   (5188 items after filters)


Optimised set:
  head       Trapper's Leather Helm  (+13 sta, +10 int, +84 armor)  https://www.wowhead.com/forever/item=252513
  neck       Ghostshard Talisman  + Necklace - Agility  (+9 sta, +14 ap)  https://www.wowhead.com/forever/item=7731
  shoulder   Pathfinder Shoulder Pads of the Bandit  (+3 agi, +7 sta, +7 ap, +71 armor)  https://www.wowhead.com/forever/item=15345?bonus=12751
  back       Tigerstrike Mantle  + Cloak - Minor Agility  (+8 agi, +7 sta, +25 armor)  https://www.wowhead.com/forever/item=13108
  chest      Raptor Hunter Tunic  + Chest - Major Stamina  (+3 agi, +16 sta, +4 str, +117 armor)  https://www.wowhead.com/forever/item=4119
  wrist      Unearthed Bands of Stamina  + Bracer - Superior Stamina  (+9 sta, +16 ap, +49 armor)  https://www.wowhead.com/forever/item=9428?bonus=13020
  hands      Razzeric's Racing Grips  + Gloves - Greater Agility  (+8 agi, +9 sta, +70 armor)  https://www.wowhead.com/forever/item=6727
  waist      Defiler's Mail Girdle  (+5 sta, +12 int, +61 armor)  https://www.wowhead.com/forever/item=20197
  legs       Necromancer Leggings  + Armor Kit - Medium/Heavy (+24/+32 armor)  (+12 sta, +11 int, +45 armor)  https://www.wowhead.com/forever/item=2277
  feet       Enchanted Sandals  + Boots - Greater Stamina  (+5 agi, +10 sta, +8 int, +36 armor)  https://www.wowhead.com/forever/item=279843
  finger     Wyvern Heart Band  (+5 agi, +5 sta, +15 ap)  https://www.wowhead.com/forever/item=285190
  finger     Lonetree's Circle  (+6 sta, +6 int, +4 spi)  https://www.wowhead.com/forever/item=18586
  trinket    Defiler's Talisman  (+6 sta)  https://www.wowhead.com/forever/item=21120
  trinket    Rune of Duty  (+4 sta)  https://www.wowhead.com/forever/item=21568
  main_hand  Clever Expeditionary's Spellblade  + Weapon - Mighty Intellect  (+4 sta, +6 int, +3 spi)  https://www.wowhead.com/forever/item=271931
  off_hand   Hillborne Axe of the Sorcerer  + Weapon - Mighty Intellect  (+3 sta, +4 int)  https://www.wowhead.com/forever/item=2080?bonus=12906
  two_hand   -
  ranged     Truthseeker's Bow  + Deadly Scope (+5 dmg)  (+7 agi, +3 sta, +23.75 dps)  https://www.wowhead.com/forever/item=277254

Totals from gear: +57 agi, +154 sta, +101 int, +7 spi, +4 str, +52 ap, +590 armor, +25.54 dps
HP 2739  EHP 2772  mana 2328  RAP 325  crit 8.2%  dodge 3.2%  DPS 147.3  shot uptime 100%  EHP x DPS 408148
```

## `python3 minmax.py set --build mm_lone_wolf --vs generic --faction horde`

```
build: mm_lone_wolf   vs: generic   (5188 items after filters)


Optimised set:
  head       Brawler's Leather Helm  (+10 agi, +13 sta, +84 armor)  https://www.wowhead.com/forever/item=252512
  neck       Ghostshard Talisman  + Necklace - Agility  (+9 sta, +14 ap)  https://www.wowhead.com/forever/item=7731
  shoulder   Pathfinder Shoulder Pads of the Bandit  (+3 agi, +7 sta, +7 ap, +71 armor)  https://www.wowhead.com/forever/item=15345?bonus=12751
  back       Tigerstrike Mantle  + Cloak - Minor Agility  (+8 agi, +7 sta, +25 armor)  https://www.wowhead.com/forever/item=13108
  chest      Garb of Fallen Felbark  + Chest - Major Stamina  (+13 agi, +7 sta, +9 int, +110 armor)  https://www.wowhead.com/forever/item=273038
  wrist      Unearthed Bands of Stamina  + Bracer - Superior Stamina  (+9 sta, +16 ap, +49 armor)  https://www.wowhead.com/forever/item=9428?bonus=13020
  hands      Razzeric's Racing Grips  + Gloves - Greater Agility  (+8 agi, +9 sta, +70 armor)  https://www.wowhead.com/forever/item=6727
  waist      Defiler's Chain Girdle  (+5 sta, +24 ap, +61 armor)  https://www.wowhead.com/forever/item=20152
  legs       Panther Hunter Leggings  + Armor Kit - Medium/Heavy (+24/+32 armor)  (+10 agi, +11 sta, +96 armor)  https://www.wowhead.com/forever/item=4108
  feet       Enchanted Sandals  + Boots - Greater Stamina  (+5 agi, +10 sta, +8 int, +36 armor)  https://www.wowhead.com/forever/item=279843
  finger     Wyvern Heart Band  (+5 agi, +5 sta, +15 ap)  https://www.wowhead.com/forever/item=285190
  finger     Determined Band  (+8 sta, +9 ap)  https://www.wowhead.com/forever/item=277208
  trinket    Defiler's Talisman  (+6 sta)  https://www.wowhead.com/forever/item=21120
  trinket    Rune of Duty  (+4 sta)  https://www.wowhead.com/forever/item=21568
  main_hand  Blade of the Magram Clan  + Weapon - Agility  (+4 sta, +10 ap)  https://www.wowhead.com/forever/item=271796
  off_hand   Scout's Blade  + Weapon - Mighty Intellect  (+7 agi, +3 sta)  https://www.wowhead.com/forever/item=19545
  two_hand   -
  ranged     Truthseeker's Bow  + Deadly Scope (+5 dmg)  (+7 agi, +3 sta, +23.75 dps)  https://www.wowhead.com/forever/item=277254

Totals from gear: +109 agi, +146 sta, +39 int, +95 ap, +634 armor, +25.54 dps
HP 2410  EHP 2892  mana 1375  RAP 358  crit 10.0%  dodge 5.0%  DPS 167.2  shot uptime 100%  EHP x DPS 483440
```

## `python3 minmax.py slots --build sv_mm_tank --vs generic --top 8`

```
build: sv_mm_tank   vs: generic   (5387 items after filters)


== head ==
   118.7  Brawler's Leather Helm                    L25 +10 agi, +13 sta, +84 armor  [crafted/drop]
   111.6  Trapper's Leather Helm                    L25 +13 sta, +10 int, +84 armor  [crafted/drop]
    99.7  Pathfinder Hat of the Bandit              L29 +4 agi, +9 sta, +11 ap, +81 armor  [drop]
    99.1  Goblin Rocket Helmet                      L10 +15 sta, +50 armor  [crafted]
    99.1  Goblin Rocket Helmet                          +15 sta, +50 armor  [crafted]
    97.5  Scaled Leather Headband of the Bandit     L27 +4 agi, +9 sta, +10 ap, +79 armor  [drop/world drop]
    94.3  Brawler's Leather Hood                    L20 +8 agi, +10 sta, +76 armor  [crafted]
    91.8  Defender's Leather Helm                   L25 +13 sta, +12 str, +84 armor  [crafted/drop]

== neck ==
    84.0  Ghostshard Talisman                       L30 +9 sta, +14 ap  [drop]
    80.5  Souvenir Sea Shell                        L30 +13 sta  [vendor]
    60.2  Darkspear Warding Pendant                 L28 +8 sta, +5 int  [vendor]
    60.2  Seal of the Expedition                    L28 +8 sta, +5 int  []
    59.9  Vermilion Necklace of the Bandit          L30 +3 agi, +6 sta, +7 ap  []
    57.7  Thermaplugg Medal of Honor                L29 +6 sta, +6 spi, +10 ap  [drop]
    56.4  Explorers' League Commendation            L28 +9 sta, +9 spi  [quest]
    56.4  Master Sergeant's Insignia                L30 +9 sta, +4 spi  [vendor]
   ench  13.5  Necklace - Agility                  +5 agi

== shoulder ==
    79.3  Watchman Pauldrons                        L27 +11 sta, +4 spi, +3 str, +80 armor  [drop]
    75.6  Pathfinder Shoulder Pads of the Bandit    L26 +3 agi, +7 sta, +7 ap, +71 armor  [drop]
    73.3  Azure Gustwoven Spaulders                 L30 +7 agi, +7 sta, +76 armor  [crafted]
    73.3  Cloudy Gustwoven Spaulders                L30 +7 agi, +7 sta, +76 armor  [crafted]
    73.3  Headhunter's Spaulders of the Monkey      L30 +7 agi, +7 sta, +76 armor  [drop]
    72.8  Headhunter's Spaulders of Stamina         L30 +10 sta, +76 armor  [drop]
    72.6  Cutthroat's Mantle of Stamina             L29 +10 sta, +75 armor  [drop]
    68.3  Headhunter's Spaulders of the Eagle       L30 +7 sta, +7 int, +76 armor  [drop]

== back ==
    77.8  Mourning Shawl                            L25 +12 sta, +24 armor  [quest]
    69.1  Tigerstrike Mantle                        L29 +8 agi, +7 sta, +25 armor  [drop]
    68.1  Grimsteel Cape                            L25 +3 agi, +9 sta, +26 armor  [quest]
    65.4  Sergeant's Cape                           L30 +9 sta, +66 armor  [vendor]
    65.4  Sergeant's Cloak                          L30 +9 sta, +66 armor  [vendor]
    63.0  Twilight Cape of the Bandit               L30 +3 agi, +6 sta, +7 ap, +23 armor  [drop]
    53.9  Vine Pruner's Cloak                       L24 +8 sta, +26 armor  [quest]
    53.5  Sparkleshell Cloak of Stamina             L30 +8 sta, +23 armor  [drop]
   ench   8.1  Cloak - Minor Agility               +3 agi

== chest ==
   122.0  Raptor Hunter Tunic                       L28 +3 agi, +16 sta, +4 str, +117 armor  [quest]
   111.0  Garb of Fallen Felbark                    L29 +13 agi, +7 sta, +9 int, +110 armor  []
   107.2  Spirewind Fetter                          L30 +11 sta, +12 int, +7 str, +112 armor  [drop]
   102.2  Cutthroat's Vest of the Bandit            L29 +4 agi, +9 sta, +11 ap, +100 armor  [drop]
   101.9  Scaled Leather Tunic of the Bandit        L28 +4 agi, +9 sta, +11 ap, +98 armor  [drop]
   100.2  Infiltrator Armor of Stamina              L30 +14 sta, +102 armor  [drop]
    99.6  Robust Tunic of the Bandit                L26 +4 agi, +9 sta, +10 ap, +95 armor  [drop]
    94.3  Infiltrator Armor of the Monkey           L30 +9 agi, +9 sta, +102 armor  [drop]
   ench  62.5  Chest - Major Stamina               +10 sta
   ench  50.3  Chest - Superior Stamina            +8 sta
   ench  44.2  Chest - Greater Stats               +4 agi, +4 sta, +4 int, +4 spi, +4 str

== wrist ==
    94.5  Unearthed Bands of Stamina                L30 +9 sta, +16 ap, +49 armor  [drop]
    83.9  Unearthed Bands of the Beast              L30 +3 agi, +6 sta, +3 str, +16 ap, +49 armor  [drop]
    81.8  Unearthed Bands of the Physician          L30 +6 sta, +3 int, +16 ap, +49 armor  [drop]
    76.0  Unearthed Bands of Arcane Protection      L30 +6 sta, +16 ap, +49 armor  [drop]
    76.0  Unearthed Bands of Frost Protection       L30 +6 sta, +16 ap, +49 armor  [drop]
    76.0  Unearthed Bands of the Champion           L30 +6 sta, +3 str, +16 ap, +49 armor  [drop]
    76.0  Unearthed Bands of the Channeler          L30 +6 sta, +3 spi, +16 ap, +49 armor  [drop]
    69.9  Cultist's Armguards                       L18 +7 sta, +10 ap, +44 armor  [quest]
   ench  56.4  Bracer - Superior Stamina           +9 sta
   ench  44.2  Bracer - Greater Stamina            +7 sta
   ench  31.7  Bracer - Stamina                    +5 sta

== hands ==
   103.5  Runebound Gloves                          L24 +10 sta, +5 spi, +16 ap, +71 armor  [quest]
    87.4  Razzeric's Racing Grips                   L29 +8 agi, +9 sta, +70 armor  [quest]
    75.9  Ebon Vise                                 L30 +6 agi, +8 sta, +4 str, +70 armor  [drop]
    74.2  Infiltrator Gloves of the Bandit          L27 +3 agi, +7 sta, +7 ap, +60 armor  [drop/world drop]
    71.7  Braced Handguards                         L30 +7 agi, +7 sta, +64 armor  [quest]
    71.5  Archer's Gloves of the Monkey             L30 +7 agi, +7 sta, +63 armor  [drop/world drop]
    71.0  Archer's Gloves of Stamina                L30 +10 sta, +63 armor  [drop/world drop]
    70.9  Headhunter's Mitts of Stamina             L29 +10 sta, +62 armor  [drop]
   ench  27.0  Gloves - Greater Agility            +10 agi
   ench  18.9  Gloves - Agility                    +7 agi

== waist ==
    86.8  Kolkar Hunter's Belt                      L30 +8 agi, +9 sta, +65 armor  [quest]
    86.7  Defiler's Chain Girdle                    L28 +5 sta, +24 ap, +61 armor  [vendor]
    86.7  Highlander's Chain Girdle                 L28 +5 sta, +24 ap, +61 armor  [vendor]
    86.1  Warden's Leather Belt                     L30 +6 agi, +9 sta, +6 str, +101 armor  [crafted]
    84.4  Defiler's Leather Girdle                  L28 +4 sta, +24 ap, +91 armor  [vendor]
    84.4  Highlander's Leather Girdle               L28 +4 sta, +24 ap, +91 armor  [vendor]
    82.4  Stalker's Leather Belt                    L30 +9 agi, +6 sta, +6 int, +4 spi, +63 armor  [crafted]
    75.7  Archer's Belt of the Bandit               L30 +3 agi, +7 sta, +8 ap, +57 armor  [drop]

== legs ==
   108.3  Panther Hunter Leggings                   L28 +10 agi, +11 sta, +96 armor  [quest]
   106.8  Headhunter's Woolies of the Bandit        L30 +4 agi, +10 sta, +11 ap, +89 armor  [drop]
   102.3  Necromancer Leggings                      L30 +12 sta, +11 int, +45 armor  [drop]
   100.3  Cutthroat's Pants of the Bandit           L28 +4 agi, +9 sta, +11 ap, +86 armor  [drop]
   100.3  Scaled Leather Leggings of the Bandit     L28 +4 agi, +9 sta, +11 ap, +86 armor  [drop]
    99.5  Triprunner Dungarees                      L25 +18 agi, +6 sta, +3 str, +101 armor  [quest]
    98.8  Supple Bellyskin Leggings                 L26 +14 sta, +6 str, +92 armor  [drop]
    98.4  Headhunter's Woolies of Stamina           L30 +14 sta, +89 armor  [drop]
   ench   4.3  Armor Kit - Medium/Heavy (+24/+32 armor) +32 armor

== feet ==
    96.6  Enchanted Sandals                         L24 +5 agi, +10 sta, +8 int, +36 armor  [quest]
    91.9  Gravewalker Boots                         L24 +7 agi, +10 sta, +7 spi, +78 armor  [quest]
    85.6  Defiler's Lizardhide Boots                L28 +5 agi, +8 sta, +4 int, +104 armor  [vendor]
    85.6  Highlander's Lizardhide Boots             L28 +5 agi, +8 sta, +4 int, +104 armor  [vendor]
    84.8  Gnomebot Operating Boots                  L29 +12 sta, +76 armor  [drop]
    83.1  Defiler's Leather Boots                   L28 +7 agi, +8 sta, +104 armor  [vendor]
    83.1  Highlander's Leather Boots                L28 +7 agi, +8 sta, +104 armor  [vendor]
    81.8  Defiler's Chain Greaves                   L28 +8 agi, +8 sta, +74 armor  [vendor]
   ench  44.2  Boots - Greater Stamina             +7 sta
   ench  31.7  Boots - Stamina                     +5 sta
   ench  25.5  Boots - Lesser Stamina              +4 sta

== finger ==
    74.4  Wyvern Heart Band                         L29 +5 agi, +5 sta, +15 ap  [drop]
    68.1  Determined Band                           L30 +8 sta, +9 ap  [quest]
    68.1  Insurgent's Band                          L28 +8 sta, +9 ap  [vendor]
    68.1  Theramore Signet                          L28 +8 sta, +9 ap  []
    63.1  Field Researcher's Loop                   L20 +7 agi, +7 sta  [quest]
    62.5  Nogg's Gold Ring                          L28 +10 sta, +4 spi  [quest]
    62.5  Rune-Etched Ring                          L24 +10 sta  [quest]
    62.5  Talvash's Gold Ring                       L28 +10 sta, +4 spi  [quest]

== trinket ==
    38.0  Defiler's Talisman                        L28 +6 sta  [vendor]
    38.0  Talisman of Arathor                       L28 +6 sta  [vendor]
    25.5  Rune of Duty                              L20 +4 sta  [vendor]
    25.5  Rune of Perfection                        L20 +4 sta  [vendor]
     0.0  Worgenbane Talisman                       L21 +2 mp5  [drop]

== main_hand ==
    45.2  Blade of the Magram Clan                  L30 +4 sta, +10 ap  [quest]
    39.0  The Butcher                               L26 +5 agi, +4 sta  [drop]
    38.8  Viking Sword of the Bandit                L25 +2 agi, +4 sta, +4 ap  [drop]
    38.8  Splitting Hatchet of the Bandit           L26 +2 agi, +4 sta, +4 ap  [drop]
    38.1  Scout's Blade                             L28 +7 agi, +3 sta  [vendor]
    38.1  Sentinel's Blade                          L28 +7 agi, +3 sta  [vendor]
    38.0  Swinetusk Shank                           L30 +6 sta, +4 spi  [drop]
    38.0  Hornbeam Heft                             L24 +6 sta, +3 spi, +3 str  [quest]
   ench  42.9  Weapon - Mighty Intellect           +22 int
   ench  40.3  Weapon - Agility                    +15 agi

== off_hand ==
    45.2  Blade of the Magram Clan                  L30 +4 sta, +10 ap  [quest]
    38.8  Splitting Hatchet of the Bandit           L26 +2 agi, +4 sta, +4 ap  [drop]
    38.1  Scout's Blade                             L28 +7 agi, +3 sta  [vendor]
    38.1  Sentinel's Blade                          L28 +7 agi, +3 sta  [vendor]
    38.0  Hornbeam Heft                             L24 +6 sta, +3 spi, +3 str  [quest]
    35.4  Scout's Blade                             L25 +6 agi, +3 sta  [vendor]
    35.4  Sentinel's Blade                          L25 +6 agi, +3 sta  [vendor]
    33.1  Serrated Raptor Claw                      L24 +5 agi, +10 ap  [quest]
   ench  42.9  Weapon - Mighty Intellect           +22 int
   ench  40.3  Weapon - Agility                    +15 agi

== two_hand ==
   123.4  Scavenged Magram Armament                 L30 +5 agi, +14 sta, +12 ap  [quest]
   121.9  Greatstaff of the Necrokhans              L30 +16 sta, +12 int, +6 spi  [quest]
    92.4  Morbid Dawn                               L30 +15 sta, +10 str  [drop]
    92.4  Staff of the Shade                        L22 +15 sta  [drop]
    90.2  Glimmering Staff                          L25 +11 sta, +11 int  [crafted]
    88.8  Acrobatic Staff of the Bandit             L29 +4 agi, +9 sta, +11 ap  [drop]
    86.5  Stonecutter Claymore of Stamina           L30 +14 sta  [drop]
    83.7  Wanderer's Broadsword                     L30 +12 sta, +1 hit  [quest]
   ench  66.7  2H Weapon - Agility                 +25 agi
   ench  42.9  Weapon - Mighty Intellect           +22 int
   ench  40.3  2H Weapon - Lesser Agility          +15 agi

== ranged ==
   229.4  Truthseeker's Bow                         L30 +7 agi, +3 sta, +23.75 dps  [quest]
   197.2  Nail Spitter                              L28 +5 sta, +4 str, +20 dps  [quest]
   184.9  Booty Bay Bruiser's Buckshot              L30 +3 sta, +9 ap, +18.04 dps  [vendor]
   176.6  Chesterfall Musket                        L28 +6 sta, +16.52 dps  [drop]
   176.4  Outrider's Bow                            L28 +2 agi, +5 sta, +16.67 dps  [vendor]
   176.4  Outrunner's Bow                           L28 +2 agi, +5 sta, +16.67 dps  [vendor]
   175.3  Master Hunter's Bow                       L28 +6 agi, +19.38 dps  [quest]
   170.7  Master Hunter's Rifle                     L28 +4 agi, +4 str, +19.42 dps  [quest]
   ench  16.0  Deadly Scope (+5 dmg)               +1.79 dps
   ench   9.6  Accurate Scope (+3 dmg)             +1.07 dps
   ench   6.4  Standard Scope (+2 dmg)             +0.71 dps

(score = duel score gain x1000 when added on top of base_gear.json)
```

