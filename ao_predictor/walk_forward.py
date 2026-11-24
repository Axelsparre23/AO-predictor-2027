from collections import defaultdict

import pandas as pd

from .backtest import classification_metrics
from .elo import DEFAULT_K, INITIAL_ELO, expected_score


def walk_forward_backtest(matches, k_factor=DEFAULT_K, hard_weight=0.35):
    """Backtest Elo using only matches from dates strictly before each match date.

    All matches on the same calendar date are predicted from the same pre-date
    ratings. Elo updates from that date are accumulated and applied together.
    """
    required = {"tourney_date", "winner_name", "loser_name", "surface"}
    missing = required.difference(matches.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if k_factor <= 0:
        raise ValueError("k_factor must be positive.")
    if not 0 <= hard_weight <= 1:
        raise ValueError("hard_weight must be between 0 and 1.")

    data = matches.copy()
    data["tourney_date"] = pd.to_datetime(data["tourney_date"], errors="coerce")
    data = data.dropna(subset=["tourney_date", "winner_name", "loser_name"])
    data = data.sort_values("tourney_date", kind="stable")

    overall = defaultdict(lambda: INITIAL_ELO)
    hard = defaultdict(lambda: INITIAL_ELO)
    predictions = []

    for match_date, day in data.groupby("tourney_date", sort=True):
        overall_delta = defaultdict(float)
        hard_delta = defaultdict(float)

        for row in day.itertuples(index=False):
            winner, loser = row.winner_name, row.loser_name
            rw = (1 - hard_weight) * overall[winner] + hard_weight * hard[winner]
            rl = (1 - hard_weight) * overall[loser] + hard_weight * hard[loser]
            p_winner = expected_score(rw, rl)

            item = {
                "tourney_date": match_date,
                "winner_name": winner,
                "loser_name": loser,
                "surface": row.surface,
                "winner_probability": p_winner,
                "outcome": 1,
            }
            if hasattr(row, "tourney_name"):
                item["tourney_name"] = row.tourney_name
            predictions.append(item)

            p_overall = expected_score(overall[winner], overall[loser])
            change = k_factor * (1 - p_overall)
            overall_delta[winner] += change
            overall_delta[loser] -= change

            if str(row.surface).lower() == "hard":
                p_hard = expected_score(hard[winner], hard[loser])
                hard_change = k_factor * (1 - p_hard)
                hard_delta[winner] += hard_change
                hard_delta[loser] -= hard_change

        for player, change in overall_delta.items():
            overall[player] += change
        for player, change in hard_delta.items():
            hard[player] += change

    result = pd.DataFrame(predictions)
    if result.empty:
        raise ValueError("No valid matches available for backtesting.")

    metrics = classification_metrics(result["winner_probability"], result["outcome"])
    metrics.update({
        "date_start": result["tourney_date"].min().date().isoformat(),
        "date_end": result["tourney_date"].max().date().isoformat(),
        "baseline_brier_score": 0.25,
        "baseline_log_loss": 0.6931471805599453,
    })
    return {"metrics": metrics, "predictions": result}
