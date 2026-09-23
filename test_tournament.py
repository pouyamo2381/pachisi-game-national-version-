import random
from tournament import TournamentBracket, TournamentError, run_full_tournament
from match_simulation import simulate_match, NUM_PLAYERS, PIECES_PER_PLAYER, TOTAL_STEPS_TO_FINISH


def test_match_simulation_terminates_and_is_valid_permutation():
    for seed in range(200):
        teams = [f"Team{seed}-{i}" for i in range(4)]
        ranking = simulate_match(teams, difficulty="Medium", seed=seed)
        assert sorted(ranking) == sorted(teams), f"seed {seed}: ranking isn't a permutation of teams"
        assert len(ranking) == 4
    print("OK: 200 simulated matches all terminated with a valid 4-team ranking")


def test_match_simulation_all_difficulties():
    for diff in ("Easy", "Medium", "Hard"):
        for seed in range(20):
            teams = [f"T{seed}"] * 0 or [f"{diff}-{seed}-{i}" for i in range(4)]
            ranking = simulate_match(teams, difficulty=diff, seed=seed)
            assert sorted(ranking) == sorted(teams)
    print("OK: Easy/Medium/Hard all produce valid results")


def test_bracket_rejects_bad_sizes():
    try:
        TournamentBracket(list(range(10)))  # 10 not divisible by 4
        assert False, "should have raised"
    except TournamentError:
        pass

    try:
        TournamentBracket(list(range(4 * 3)))  # 3 groups -> not a power of 2
        assert False, "should have raised"
    except TournamentError:
        pass
    print("OK: bracket rejects team counts that can't shrink cleanly to one final")


def test_bracket_small_manual():
    # 4 groups of 4 = 16 teams -> round1 (4 matches) -> round2 (1 final match)
    teams = list(range(16))
    b = TournamentBracket(teams)
    assert len(b.current_groups) == 4
    assert not b.is_complete

    # Round 1: top2 of each group (by construction: lowest two ids "win")
    for i, group in enumerate(list(b.current_groups)):
        ranked = sorted(group)  # pretend lower id always finishes better, for a deterministic test
        b.record_match_result(i, ranked)

    assert not b.is_complete
    assert len(b.current_groups) == 2, "4 groups -> top2 each -> 8 teams -> 2 new groups of 4"
    for i, group in enumerate(list(b.current_groups)):
        ranked = sorted(group)
        b.record_match_result(i, ranked)
    assert not b.is_complete
    assert len(b.current_groups) == 1 and b.is_final_round
    ranked = sorted(b.current_groups[0])
    b.record_match_result(0, ranked)
    assert b.is_complete
    assert b.champion_ranking[0] == 0
    print("OK: 16-team bracket (4 groups) shrinks 4 -> 2 -> 1 exactly as described")


def test_bracket_pairing_shape_64_teams():
    teams = list(range(64))
    b = TournamentBracket(teams)
    assert len(b.rounds[0]) == 16
    # simulate round 1: team with the lower id in each group of 4 finishes 1st, then next id, etc.
    for i, group in enumerate(list(b.current_groups)):
        ranked = sorted(group)
        b.record_match_result(i, ranked)
    assert len(b.current_groups) == 8, f"expected 8 groups after round 1, got {len(b.current_groups)}"
    for i, group in enumerate(list(b.current_groups)):
        ranked = sorted(group)
        b.record_match_result(i, ranked)
    assert len(b.current_groups) == 4
    for i, group in enumerate(list(b.current_groups)):
        ranked = sorted(group)
        b.record_match_result(i, ranked)
    assert len(b.current_groups) == 2
    for i, group in enumerate(list(b.current_groups)):
        ranked = sorted(group)
        b.record_match_result(i, ranked)
    assert len(b.current_groups) == 1
    assert b.is_final_round
    final_group = b.current_groups[0]
    ranked = sorted(final_group)
    b.record_match_result(0, ranked)
    assert b.is_complete
    assert b.champion_ranking[0] == 0  # team 0 always "wins" in this deterministic test
    print("OK: 64-team bracket shrinks 16 -> 8 -> 4 -> 2 -> 1 exactly as described, champion =", b.champion_ranking[0])


def test_full_tournament_with_real_match_engine_64_teams():
    countries = [f"Country{i}" for i in range(64)]

    def play(group):
        return simulate_match(group, difficulty="Medium", seed=random.randint(0, 10**9))

    bracket = run_full_tournament(countries, play)
    assert bracket.is_complete
    assert len(bracket.champion_ranking) == 4
    assert len(set(bracket.champion_ranking)) == 4
    print("OK: full 64-team tournament (16 groups -> ... -> final) completed using the real match engine.")
    print("Champion:", bracket.champion_ranking[0])
    print("2nd:", bracket.champion_ranking[1])
    print("3rd:", bracket.champion_ranking[2])
    print("4th:", bracket.champion_ranking[3])
    print()
    print(bracket.describe()[-800:])


if __name__ == "__main__":
    test_match_simulation_terminates_and_is_valid_permutation()
    test_match_simulation_all_difficulties()
    test_bracket_rejects_bad_sizes()
    test_bracket_small_manual()
    test_bracket_pairing_shape_64_teams()
    test_full_tournament_with_real_match_engine_64_teams()
    print("\nALL TESTS PASSED")
