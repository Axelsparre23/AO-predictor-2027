import pandas as pd
import pytest

from ao_predictor.walk_forward import walk_forward_backtest


def test_same_day_matches_use_identical_pre_day_ratings():
    matches = pd.DataFrame([
        {"tourney_date": "2024-01-01", "winner_name": "A", "loser_name": "B", "surface": "Hard"},
        {"tourney_date": "2024-01-01", "winner_name": "A", "loser_name": "C", "surface": "Hard"},
        {"tourney_date": "2024-01-02", "winner_name": "A", "loser_name": "B", "surface": "Hard"},
    ])
    result = walk_forward_backtest(matches)
    p = result["predictions"]["winner_probability"]
    assert p.iloc[0] == pytest.approx(0.5)
    assert p.iloc[1] == pytest.approx(0.5)
    assert p.iloc[2] > 0.5
    assert result["metrics"]["n"] == 3


def test_backtest_requires_columns():
    with pytest.raises(ValueError, match="Missing required columns"):
        walk_forward_backtest(pd.DataFrame({"winner_name": ["A"]}))


def test_backtest_rejects_empty_data():
    empty = pd.DataFrame(columns=["tourney_date", "winner_name", "loser_name", "surface"])
    with pytest.raises(ValueError, match="No valid matches"):
        walk_forward_backtest(empty)


def test_backtest_rejects_invalid_hard_weight():
    matches = pd.DataFrame([
        {"tourney_date": "2024-01-01", "winner_name": "A", "loser_name": "B", "surface": "Hard"}
    ])
    with pytest.raises(ValueError, match="hard_weight"):
        walk_forward_backtest(matches, hard_weight=1.5)
