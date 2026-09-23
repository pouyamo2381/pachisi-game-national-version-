"""
tournament.py
--------------
Manages a "World Cup" style Manchi/Ludo tournament.

Format (exactly as described):
  - Teams start in groups of 4. Each group plays ONE match.
  - The top 2 finishers of a match advance.
  - Two advancing pairs (from two different groups) are combined into a
    new group of 4 for the next round.
  - This repeats until only one group of 4 remains: the FINAL. Its
    result decides places 1st through 4th.

This module has NO dependency on pygame - it only tracks team ids/objects
and match rankings - so it can be unit tested and reused independently of
the game's graphics.

Requirement: the number of first-round groups (len(teams) / group_size)
must be a power of two, so the bracket shrinks cleanly to a single final
without any byes. 16 groups of 4 (64 teams) is the classic case Peter
described:  16 -> 8 -> 4 -> 2 -> 1.
"""

from typing import List, Optional, Sequence


class TournamentError(Exception):
    """Raised for structural problems with the bracket (bad sizes, mismatched results)."""


class TournamentBracket:
    def __init__(self, teams: Sequence, group_size: int = 4, advance_per_match: int = 2):
        if len(teams) == 0:
            raise TournamentError("Need at least one team.")
        if len(teams) % group_size != 0:
            raise TournamentError(
                f"Number of teams ({len(teams)}) is not divisible by group size ({group_size})."
            )

        num_groups = len(teams) // group_size
        if num_groups & (num_groups - 1) != 0:
            raise TournamentError(
                f"Number of first-round groups ({num_groups}) must be a power of 2 "
                f"(1, 2, 4, 8, 16, ...) so the bracket can shrink cleanly to a single "
                f"final without byes. {len(teams)} teams / {group_size} per group = "
                f"{num_groups} groups, which is not a power of 2."
            )
        if advance_per_match * (num_groups // 1) < 0:  # defensive, kept simple
            pass
        if group_size % advance_per_match != 0:
            raise TournamentError(
                "group_size must be a multiple of advance_per_match so that pairing "
                "advancing teams into new groups comes out even."
            )

        self.group_size = group_size
        self.advance_per_match = advance_per_match

        first_round_groups = [
            list(teams[i:i + group_size]) for i in range(0, len(teams), group_size)
        ]
        self.rounds: List[List[List]] = [first_round_groups]
        self.round_results: List[List[Optional[List]]] = [
            [None] * len(first_round_groups)
        ]
        self.current_round = 0
        self.champion_ranking: Optional[List] = None

    # Queries 

    @property
    def current_groups(self) -> List[List]:
        return self.rounds[self.current_round]

    @property
    def is_final_round(self) -> bool:
        return len(self.current_groups) == 1

    @property
    def is_complete(self) -> bool:
        return self.champion_ranking is not None

    @property
    def round_name(self) -> str:
        """Friendly label for the current round: 'Stage 1', 'Stage 2', ...,
        'Quarterfinal', 'Semifinal', 'Final' - counted from the very first
        round (whatever its group count is) down to the single-group final."""
        import math
        n = len(self.current_groups)
        total_first_round_groups = len(self.rounds[0])

        if n == total_first_round_groups:
            return "Stage 1"
        if n == 1:
            return "Final"
        if n == 2:
            return "Semifinal"
        if n == 4:
            return "Quarterfinal"

        max_halvings = int(math.log2(total_first_round_groups))
        halvings_to_final = int(math.log2(n))
        stage_num = max_halvings - halvings_to_final + 1
        return f"Stage {stage_num}"

    def next_unplayed_match_index(self) -> Optional[int]:
        """Index of the next group in the current round with no recorded result, or None."""
        for i, r in enumerate(self.round_results[self.current_round]):
            if r is None:
                return i
        return None

    def is_round_complete(self) -> bool:
        return self.next_unplayed_match_index() is None

    #  Recording results

    def record_match_result(self, group_index: int, ranked_teams: Sequence) -> None:
        """
        ranked_teams: the group's teams, reordered 1st place first, last place last.
        Must be exactly the same set of teams as the group (order doesn't matter
        for validation, only for what you pass in).
        """
        if self.is_complete:
            raise TournamentError("Tournament is already finished; nothing left to record.")

        group = self.current_groups[group_index]
        if sorted(map(repr, ranked_teams)) != sorted(map(repr, group)):
            raise TournamentError(
                f"Result for group {group_index} doesn't match its teams.\n"
                f"Group has: {group}\nResult given: {list(ranked_teams)}"
            )

        self.round_results[self.current_round][group_index] = list(ranked_teams)

        if self.is_round_complete():
            self._advance_round()

    #  Internal 

    def _advance_round(self) -> None:
        results = self.round_results[self.current_round]

        if len(results) == 1:
            self.champion_ranking = results[0]
            return

        advancing = []
        for ranked in results:
            advancing.extend(ranked[: self.advance_per_match])

        next_groups = [
            advancing[i:i + self.group_size]
            for i in range(0, len(advancing), self.group_size)
        ]

        self.rounds.append(next_groups)
        self.round_results.append([None] * len(next_groups))
        self.current_round += 1

    #  Reporting 

    def standings_summary(self):
        """List of (round_index, group_index, ranked_teams_or_None) for a progress display."""
        summary = []
        for rnd_idx, results in enumerate(self.round_results):
            for grp_idx, ranked in enumerate(results):
                summary.append((rnd_idx, grp_idx, ranked))
        return summary

    def describe(self) -> str:
        lines = []
        for rnd_idx, groups in enumerate(self.rounds):
            results = self.round_results[rnd_idx]
            label = "Final" if len(groups) == 1 else f"Round {rnd_idx + 1} ({len(groups)} groups)"
            lines.append(label)
            for i, group in enumerate(groups):
                res = results[i]
                if res is None:
                    lines.append(f"  Group {i}: {group}  -> not played yet")
                else:
                    lines.append(f"  Group {i}: {group}  -> result: {res}")
        if self.champion_ranking:
            lines.append("")
            lines.append(f"CHAMPION: {self.champion_ranking[0]}")
            lines.append(f"2nd: {self.champion_ranking[1]}")
            lines.append(f"3rd: {self.champion_ranking[2]}")
            lines.append(f"4th: {self.champion_ranking[3]}")
        return "\n".join(lines)

    # Persistence 

    def to_dict(self) -> dict:
        """Plain-dict snapshot of the whole bracket, safe to json.dump()."""
        return {
            "group_size": self.group_size,
            "advance_per_match": self.advance_per_match,
            "rounds": self.rounds,
            "round_results": self.round_results,
            "current_round": self.current_round,
            "champion_ranking": self.champion_ranking,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TournamentBracket":
        """Rebuilds a bracket exactly as it was from to_dict() output - used to
        resume a tournament after a save/load, without replaying any matches."""
        obj = cls.__new__(cls)
        obj.group_size = data["group_size"]
        obj.advance_per_match = data["advance_per_match"]
        obj.rounds = data["rounds"]
        obj.round_results = data["round_results"]
        obj.current_round = data["current_round"]
        obj.champion_ranking = data["champion_ranking"]
        return obj


def run_full_tournament(teams: Sequence, play_match_fn, group_size: int = 4,
                         advance_per_match: int = 2) -> "TournamentBracket":
    """
    Convenience driver: repeatedly asks play_match_fn(group) -> ranked_list
    for every unplayed match until the bracket is complete. Useful for
    headless simulation or automated testing.
    """
    bracket = TournamentBracket(teams, group_size=group_size, advance_per_match=advance_per_match)
    while not bracket.is_complete:
        idx = bracket.next_unplayed_match_index()
        group = bracket.current_groups[idx]
        ranked = play_match_fn(group)
        bracket.record_match_result(idx, ranked)
    return bracket