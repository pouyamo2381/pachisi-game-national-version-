"""
run_world_cup_demo.py
----------------------
Demonstrates the tournament format end-to-end with the real 64-country list
(the original 49 + Peter's 5 new additions + 10 more added to round out to 64),
using the actual match engine (match_simulation.py) - not a fake/deterministic
stand-in - so this is a genuine dry run of the whole bracket:

    16 groups of 4  ->  8 groups of 4  ->  4 groups of 4  ->  2 groups of 4  ->  Final

Run it with:  python3 run_world_cup_demo.py
(Optionally: python3 run_world_cup_demo.py <seed>  for a repeatable result.)
"""

import sys
import random

from tournament import TournamentBracket
from match_simulation import simulate_match

# Same 64 countries as ALL_COUNTRIES_DATA in the game file, names only
# (in id order 0..63) - kept separate here so this demo runs with no
# pygame/display dependency at all.
COUNTRY_NAMES = [
    "Algeria", "Argentina", "Australia", "Austria", "Brazil", "Cambodia", "Canada", "Chile",
    "China", "Czech Republic", "Denmark", "Ecuador", "Egypt", "Estonia", "Finland", "France",
    "Germany", "India", "Iran", "Ireland", "Israel", "Italy", "Japan", "Kazakhstan",
    "Mexico", "Morocco", "Nepal", "Netherlands", "New Zealand", "Nigeria", "Norway", "Panama",
    "Poland", "Portugal", "Saudi Arabia", "South Africa", "South Korea", "Spain", "Sweden",
    "Switzerland", "Tajikistan", "Thailand", "Tunisia", "Turkey", "Turkmenistan", "UAE", "UK",
    "USA", "Uruguay",
    # Added to reach 64:
    "Peru", "Ghana", "Colombia", "Slovakia", "New Caledonia", "Jordan", "Uzbekistan",
    "Croatia", "Belgium", "Venezuela", "Cuba", "Malaysia", "Costa Rica", "Cameroon", "England",
]
assert len(COUNTRY_NAMES) == 64


def letter_for_group(index: int) -> str:
    return chr(ord('A') + index)


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else None
    rng = random.Random(seed)

    teams = list(COUNTRY_NAMES)
    rng.shuffle(teams)  # random draw, like pulling names out of the World Cup bowls

    bracket = TournamentBracket(teams, group_size=4, advance_per_match=2)

    round_num = 1
    while not bracket.is_complete:
        print(f"\n===== {bracket.round_name} =====")
        groups = bracket.current_groups
        for i, group in enumerate(groups):
            label = letter_for_group(i) if len(groups) <= 16 else str(i + 1)
            ranked = simulate_match(group, difficulty="Medium", seed=rng.randint(0, 10**9))
            bracket.record_match_result(i, ranked)
            print(f"  Group {label}: {', '.join(group)}")
            print(f"    -> 1st {ranked[0]}  2nd {ranked[1]}  (advance)   "
                  f"3rd {ranked[2]}  4th {ranked[3]}  (eliminated)")
        round_num += 1

    champ = bracket.champion_ranking
    print("\n================ FINAL RESULT ================")
    print(f"  Champion : {champ[0]}")
    print(f"  2nd place: {champ[1]}")
    print(f"  3rd place: {champ[2]}")
    print(f"  4th place: {champ[3]}")
    print("================================================")


if __name__ == "__main__":
    main()
