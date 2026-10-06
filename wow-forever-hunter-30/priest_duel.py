#!/usr/bin/env python3
"""Hunter vs priest duel simulator (WoW Forever, level 30).

Tracks both health and mana bars second by second, with a simple priest healing AI
(Penance on cooldown, Power Word: Shield, Heal / Flash Heal, Desperate Prayer, a potion)
and several hunter strategies. Priest spell numbers are Forever level-30 values from Wowhead.
Character numbers marked PLACEHOLDER in priest_duel.json are guesses: replace them with
what you see in game.

Usage:
  python3 priest_duel.py                 # compare all strategies
  python3 priest_duel.py --trace burst   # second-by-second log for one strategy
  python3 priest_duel.py --set hunter.auto_dps=60 --set priest.mana=1800
"""
import argparse
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def simulate(cfg, strategy, trace=False):
    h, p, s = dict(cfg["hunter"]), dict(cfg["priest"]), cfg["spells"]
    hp_h, mana_h = h["hp"], h["mana"]
    hp_p, mana_p = p["hp"], p["mana"]
    shield = 0.0
    weakened_until = -1
    cd = {"penance": 0, "dismember": h["dismember_first_at"], "rapid": 0, "desperate": 0, "potion": 0,
          "potion_h": 0}
    dismember_until = -1
    rapid_until = -1
    channel = []          # pending Penance ticks: list of (time, amount)
    casting_until = 0      # priest busy casting a heal
    pending_heal = None    # (finish_time, amount)
    inner_fire = p["inner_fire_charges"]
    marked = False
    log = []
    t = 0
    dt = 1
    while t < cfg["max_sec"]:
        heal_mult = 0.5 if t < dismember_until else 1.0

        # ---------- hunter ----------
        if not marked and mana_h >= s["hunters_mark_mana"]:
            mana_h -= s["hunters_mark_mana"]
            marked = True
        ap_bonus_dps = s["hunters_mark_dps"] if marked else 0
        free = h["auto_dps"] * (s["rapid_fire_speed"] if t < rapid_until else 1) + ap_bonus_dps
        armor_mult = 1 - (p["inner_fire_dr"] if inner_fire > 0 else 0)
        dmg = free * armor_mult + h["pet_dps"]
        inner_fire -= h["hits_per_sec"]

        if cd["dismember"] <= t and h["has_dismember"]:
            dismember_until = t + s["dismember_sec"]
            cd["dismember"] = t + s["dismember_cd"]
        window = t < dismember_until or hp_p < p["hp"] * h["execute_frac"]
        spend = 0.0
        if strategy == "spam":
            spend = h["shot_mana_per_sec"]
        elif strategy == "burst":
            if window:
                spend = h["shot_mana_per_sec"] * 1.5
                if cd["rapid"] <= t:
                    rapid_until, cd["rapid"] = t + 15, t + 300
        elif strategy == "free_only":
            spend = 0.0
        elif strategy == "sting_only":
            spend = s["serpent_mana"] / 15
        spend = min(spend, mana_h)
        mana_h -= spend
        dmg += spend * h["shot_dmg_per_mana"] * armor_mult if strategy != "sting_only" else spend * s["serpent_dmg_per_mana"]

        # shield absorbs first
        absorbed = min(shield, dmg)
        shield -= absorbed
        hp_p -= dmg - absorbed

        # ---------- priest ----------
        # finish heals
        for tick_t, amt in list(channel):
            if tick_t <= t:
                hp_p = min(p["hp"], hp_p + amt * heal_mult)
                channel.remove((tick_t, amt))
        if pending_heal and pending_heal[0] <= t:
            hp_p = min(p["hp"], hp_p + pending_heal[1] * heal_mult)
            pending_heal = None

        busy = t < casting_until
        missing = p["hp"] - hp_p
        healed_this_sec = False
        if hp_p <= 0:
            pass
        elif hp_p < p["hp"] * 0.3 and cd["desperate"] <= t:
            hp_p += s["desperate_prayer"] * heal_mult
            cd["desperate"] = t + 600
        elif hp_p < p["hp"] * 0.35 and cd["potion"] <= t and p["potions"] > 0:
            hp_p += s["potion_heal"] * heal_mult
            cd["potion"] = t + 120
            p["potions"] -= 1
        if hp_p > 0 and not busy:
            if missing >= s["penance_tick"] * 2 and cd["penance"] <= t and mana_p >= s["penance_mana"]:
                mana_p -= s["penance_mana"]
                channel += [(t, s["penance_tick"]), (t + 1, s["penance_tick"]), (t + 2, s["penance_tick"])]
                cd["penance"] = t + s["penance_cd"]
                casting_until = t + 2
                healed_this_sec = True
            elif shield <= 0 and t >= weakened_until and missing > 150 and mana_p >= s["shield_mana"]:
                mana_p -= s["shield_mana"]
                shield = s["shield_absorb"]
                weakened_until = t + s["weakened_soul_sec"]
                healed_this_sec = True
            elif missing >= s["heal_avg"] * heal_mult * 0.9 and mana_p >= s["heal_mana"]:
                mana_p -= s["heal_mana"]
                pending_heal = (t + s["heal_cast"], s["heal_avg"])
                casting_until = t + s["heal_cast"]
                healed_this_sec = True
            elif hp_p < p["hp"] * 0.4 and mana_p >= s["flash_mana"]:
                mana_p -= s["flash_mana"]
                pending_heal = (t + 2, s["flash_avg"])
                casting_until = t + 2
                healed_this_sec = True

        # priest offence when not healing
        if hp_p > 0 and not healed_this_sec and t >= casting_until:
            if mana_p > p["mana"] * p["offense_mana_floor"]:
                cost = p["offense_mana_per_sec"]
                mana_p -= cost
                hp_h -= p["offense_dps"]
                if p["mana_burn"] and mana_h > 0:
                    burn = min(mana_h, p["mana_burn_per_sec"])
                    mana_h -= burn
            else:
                hp_h -= p["wand_dps"]
        else:
            hp_h -= p["dot_dps"]
        if hp_h < h["hp"] * 0.35 and cd["potion_h"] <= t and h["potions"] > 0:
            hp_h += s["potion_heal"]
            cd["potion_h"] = t + 120
            h["potions"] -= 1
        mana_p = min(p["mana"], mana_p + p["mp5"] / 5)
        mana_h = min(h["mana"], mana_h + h["mp5"] / 5)

        if trace:
            log.append(f"{t:4d}s  hunter {max(hp_h,0):5.0f} hp {mana_h:5.0f} mp | priest {max(hp_p,0):5.0f} hp "
                       f"{mana_p:5.0f} mp shield {shield:3.0f}{'  DISMEMBER' if t < dismember_until else ''}")
        if hp_p <= 0 or hp_h <= 0:
            break
        t += dt
    winner = "hunter" if hp_p <= 0 else ("priest" if hp_h <= 0 else "timeout")
    return dict(winner=winner, t=t, hp_h=max(hp_h, 0), hp_p=max(hp_p, 0), mana_h=mana_h, mana_p=mana_p, log=log)


def setval(cfg, expr):
    key, val = expr.split("=", 1)
    node = cfg
    parts = key.split(".")
    for k in parts[:-1]:
        node = node[k]
    node[parts[-1]] = json.loads(val)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--trace", help="print a second-by-second log for this strategy")
    ap.add_argument("--set", action="append", default=[], help="override a value, e.g. hunter.auto_dps=60")
    a = ap.parse_args()
    cfg = json.load(open(os.path.join(HERE, "priest_duel.json")))
    for e in a.set:
        setval(cfg, e)
    strategies = {
        "spam": "fire mana shots nonstop",
        "free_only": "Hunter's Mark, then Auto Shot + pet only",
        "sting_only": "Hunter's Mark + keep Serpent Sting up",
        "burst": "save mana; dump it (plus Rapid Fire) during Dismember and when the priest is low",
    }
    if a.trace:
        r = simulate(cfg, a.trace, trace=True)
        print("\n".join(r["log"]))
        print(f"\n{r['winner']} after {r['t']}s")
        return
    print(f"{'strategy':11s} {'result':8s} {'time':>5s}  {'hunter hp/mp':>14s}  {'priest hp/mp':>14s}")
    for k, desc in strategies.items():
        r = simulate(cfg, k)
        print(f"{k:11s} {r['winner']:8s} {r['t']:4d}s  {r['hp_h']:6.0f}/{r['mana_h']:<6.0f}  {r['hp_p']:6.0f}/{r['mana_p']:<6.0f}   {desc}")


if __name__ == "__main__":
    main()
