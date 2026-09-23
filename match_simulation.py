"""
match_simulation.py
--------------------
A headless (no pygame, no graphics) engine that plays out ONE 4-team Manchi
(Ludo) match and returns the final ranking, 1st place through 4th.

This is deliberately independent from the pixel-coordinate board in the
main game file. It uses the standard abstract Ludo model:

  - A shared 52-square outer track.
  - Each of the 4 players enters the track 13 squares apart from the next
    (52 / 4 = 13), so all four "laps" are the same shape, just rotated.
  - Each piece needs to travel 51 squares on the shared track and then
    6 more squares up its own coloured home stretch: 57 steps total.
    Landing on step 57 exactly finishes the piece (overshooting is an
    illegal move, same as classic Ludo).
  - Rolling a 6 lets a piece leave base, and grants the player another
    roll afterwards.
  - Landing exactly on an opponent (while still on the shared track, and
    not on a safe square) sends that opponent's piece back to base.
  - Safe squares: every player's own entry square, plus one "star" square
    8 steps after each entry square (8 total safe squares) - this matches
    the star squares marked on the board in the pygame version.

Why a separate engine instead of reusing the pygame Piece class: the
Piece class is written around this game's pixel board and pygame timers
(animation, sound). None of that is needed to decide who finishes 1st
through 4th, and keeping this engine free of pygame means the tournament
bracket logic can be tested and run without a display - the actual
graphical Piece/board code in the main file is what you use when a
person wants to *watch and click through* an individual match.
"""

import random
from dataclasses import dataclass, field
from typing import List, Optional, Sequence

MAIN_TRACK_LEN = 52
HOME_STRETCH_LEN = 6
TOTAL_STEPS_TO_FINISH = MAIN_TRACK_LEN - 1 + HOME_STRETCH_LEN  # 57
PIECES_PER_PLAYER = 4
NUM_PLAYERS = 4
ENTRY_SPACING = MAIN_TRACK_LEN // NUM_PLAYERS  # 13

SAFE_TRACK_POSITIONS = {p * ENTRY_SPACING for p in range(NUM_PLAYERS)} | {
    (p * ENTRY_SPACING + 8) % MAIN_TRACK_LEN for p in range(NUM_PLAYERS)
}

BASE = -1
FINISHED = TOTAL_STEPS_TO_FINISH


@dataclass
class _Piece:
    player_index: int
    progress: int = BASE  # -1 = in base, 0..50 = on shared track, 51..56 = home stretch, 57 = finished

    @property
    def in_base(self) -> bool:
        return self.progress == BASE

    @property
    def is_finished(self) -> bool:
        return self.progress == FINISHED

    @property
    def on_shared_track(self) -> bool:
        return 0 <= self.progress <= MAIN_TRACK_LEN - 2  # 0..50

    def global_track_position(self) -> int:
        """Only meaningful while on_shared_track is True."""
        return (self.progress + self.player_index * ENTRY_SPACING) % MAIN_TRACK_LEN


def _potential_target(piece: _Piece, roll: int) -> Optional[int]:
    """Returns the new progress value for `piece` after rolling `roll`, or None if illegal."""
    if piece.is_finished:
        return None
    if piece.in_base:
        return 0 if roll == 6 else None
    target = piece.progress + roll
    if target > TOTAL_STEPS_TO_FINISH:
        return None  # must roll the exact number to finish - overshoot is illegal
    return target


def _is_vulnerable(pieces: List[_Piece], mover_index: int, target_progress: int) -> bool:
    """Would landing on `target_progress` (a shared-track progress value) be capturable
    next turn by any opponent piece already on the board?"""
    temp = _Piece(mover_index, target_progress)
    if not temp.on_shared_track or temp.global_track_position() in SAFE_TRACK_POSITIONS:
        return False
    target_global = temp.global_track_position()

    for opp in pieces:
        if opp.player_index == mover_index or opp.in_base or opp.is_finished:
            continue
        if not opp.on_shared_track:
            continue
        for roll in range(1, 7):
            opp_target = _potential_target(opp, roll)
            if opp_target is None:
                continue
            opp_after = _Piece(opp.player_index, opp_target)
            if opp_after.on_shared_track and opp_after.global_track_position() == target_global:
                return True
    return False


def _choose_move(pieces: List[_Piece], player_index: int, roll: int, difficulty: str,
                  rng: random.Random):
    """Mirrors the scoring style of the main game's AI: prefer finishing, capturing,
    leaving base on a 6, and reaching safe squares; avoid leaving a piece exposed."""
    candidates = []
    my_pieces = [p for p in pieces if p.player_index == player_index]

    for piece in my_pieces:
        target = _potential_target(piece, roll)
        if target is None:
            continue

        score = 0.0
        if piece.in_base and roll == 6:
            score = 1000.0
        else:
            if target == FINISHED:
                score = max(score, 990.0)

            temp = _Piece(player_index, target)
            captured_someone = False
            if temp.on_shared_track and temp.global_track_position() not in SAFE_TRACK_POSITIONS:
                for opp in pieces:
                    if (opp.player_index != player_index and opp.on_shared_track
                            and opp.global_track_position() == temp.global_track_position()):
                        captured_someone = True
                if captured_someone:
                    score = max(score, 900.0)

            if difficulty == "Easy":
                if score < 100:
                    score = 50.0
            else:
                if temp.progress >= MAIN_TRACK_LEN - 1:  # entered home stretch
                    score = max(score, 700.0 + (temp.progress - (MAIN_TRACK_LEN - 1)) * 10)
                if temp.on_shared_track and temp.global_track_position() in SAFE_TRACK_POSITIONS:
                    score = max(score, 600.0)
                score = max(score, 300.0 + target)
                if _is_vulnerable(pieces, player_index, target):
                    score -= 500.0

        score += rng.uniform(0, 4.9)
        candidates.append((piece, target, score))

    if not candidates:
        return None, None
    candidates.sort(key=lambda c: c[2], reverse=True)
    best = candidates[0]
    return best[0], best[1]


def simulate_match(team_ids: Sequence, difficulty: str = "Medium", seed: Optional[int] = None,
                    max_turns: int = 4000) -> List:
    """
    Plays one full 4-team match headlessly and returns team_ids reordered
    1st place first .. 4th place last.

    team_ids: exactly 4 identifiers (country ids, names, whatever the caller uses).
    difficulty: "Easy" | "Medium" | "Hard" - only changes how sharp the AI's
                move choice is (mirrors the main game's three levels).
    seed: pass an int for a reproducible result (useful for tests); leave
          None for a normal random match.
    """
    if len(team_ids) != NUM_PLAYERS:
        raise ValueError(f"simulate_match needs exactly {NUM_PLAYERS} teams, got {len(team_ids)}.")

    rng = random.Random(seed)
    pieces = [_Piece(player_index=p) for p in range(NUM_PLAYERS) for _ in range(PIECES_PER_PLAYER)]
    finish_order: List[int] = []
    current_player = 0
    turns_taken = 0

    def pieces_finished(player_index: int) -> int:
        return sum(1 for pc in pieces if pc.player_index == player_index and pc.is_finished)

    while len(finish_order) < NUM_PLAYERS - 1 and turns_taken < max_turns:
        turns_taken += 1

        if current_player in finish_order:
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        roll = rng.randint(1, 6)
        piece, target = _choose_move(pieces, current_player, roll, difficulty, rng)

        if piece is not None:
            if target == FINISHED:
                piece.progress = FINISHED
            else:
                if 0 <= target <= MAIN_TRACK_LEN - 2:
                    landed_global = _Piece(current_player, target).global_track_position()
                    if landed_global not in SAFE_TRACK_POSITIONS:
                        for opp in pieces:
                            if (opp.player_index != current_player and opp.on_shared_track
                                    and opp.global_track_position() == landed_global):
                                opp.progress = BASE
                piece.progress = target

            if pieces_finished(current_player) == PIECES_PER_PLAYER and current_player not in finish_order:
                finish_order.append(current_player)

        # Extra turn on a 6, otherwise move to the next player not yet finished.
        if roll != 6 or current_player in finish_order:
            nxt = (current_player + 1) % NUM_PLAYERS
            while nxt in finish_order:
                nxt = (nxt + 1) % NUM_PLAYERS
            current_player = nxt

    ranking_indices = list(finish_order)
    for p in range(NUM_PLAYERS):
        if p not in ranking_indices:
            ranking_indices.append(p)

    return [team_ids[i] for i in ranking_indices]
