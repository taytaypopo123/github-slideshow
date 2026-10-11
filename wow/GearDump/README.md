# GearDump

A small WoW addon that saves your equipped gear, the equippable items in your bags, and your key stats (health, Agility, Stamina, armor, ranged attack power, crit) to a file Claude can read.

It only records what you're wearing. It doesn't automate anything.

## Install

1. Copy the `GearDump` folder into your WoW AddOns folder:
   `World of Warcraft/<game version folder>/Interface/AddOns/GearDump/`
   (the folder must contain `GearDump.toc` and `GearDump.lua` directly).
2. At the character select screen, open **AddOns** and enable **GearDump**.
   If it shows as "out of date", tick **Load out of date AddOns**. The `## Interface` number in the `.toc` may not match the Forever client yet.

## Use

- It snapshots automatically on login, every time you change gear, and on logout.
- WoW only writes the file to disk on `/reload` or logout, so after swapping gear type `/reload`.
- `/geardump` prints how many items it captured.

## Where the file is

```
World of Warcraft/<game version folder>/WTF/Account/<ACCOUNT>/SavedVariables/GearDump.lua
```

It contains a `GearDumpDB` table keyed by `Name-Realm`, with `equipped` (by slot, with item ID and link), `bags`, and `stats`.

## Asking Claude

In a Claude session running on your computer, say something like:

> Read my GearDump file at `<path above>`, look up each item on Wowhead Forever (`https://www.wowhead.com/forever/item=<id>?xml`), compare it with my Hunter 30 Twink Hub (https://claude.ai/artifact/25dBkJzqvfhrFX5WBNcmEN) and tell me which slots to upgrade next.
