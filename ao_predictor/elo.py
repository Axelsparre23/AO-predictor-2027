from collections import defaultdict

INITIAL_ELO = 1500.0
DEFAULT_K = 32.0

def expected_score(rating_a: float, rating_b: float) -> float:
    return 1.0 / (1.0 + 10.0 ** ((rating_b - rating_a) / 400.0))

def build_ratings(matches, k_factor: float = DEFAULT_K):
    """Calculate chronological overall and hard-court Elo ratings."""
    overall = defaultdict(lambda: INITIAL_ELO)
    hard = defaultdict(lambda: INITIAL_ELO)
    for row in matches.itertuples(index=False):
        winner, loser = row.winner_name, row.loser_name
        ew = expected_score(overall[winner], overall[loser])
        overall[winner] += k_factor * (1 - ew)
        overall[loser] -= k_factor * (1 - ew)
        if str(row.surface).lower() == "hard":
            eh = expected_score(hard[winner], hard[loser])
            hard[winner] += k_factor * (1 - eh)
            hard[loser] -= k_factor * (1 - eh)
    return overall, hard

def player_rating(name: str, overall, hard, hard_weight: float = 0.35) -> float:
    return (1 - hard_weight) * overall[name] + hard_weight * hard[name]
