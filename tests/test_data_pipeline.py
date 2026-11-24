import pandas as pd
import pytest
from ao_predictor.data import load_matches

def test_loader_rejects_missing_directory(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_matches(tmp_path, "atp")

def test_loader_sorts_and_parses_dates(tmp_path):
    pd.DataFrame([
        {"tourney_date": 20250108, "winner_name": "B", "loser_name": "A", "surface": "Hard"},
        {"tourney_date": 20250102, "winner_name": "A", "loser_name": "B", "surface": "Clay"},
    ]).to_csv(tmp_path / "atp_matches_2025.csv", index=False)
    result = load_matches(tmp_path, "atp")
    assert result.iloc[0].winner_name == "A"
    assert str(result.iloc[0].tourney_date.date()) == "2025-01-02"

def test_loader_rejects_invalid_tour(tmp_path):
    with pytest.raises(ValueError):
        load_matches(tmp_path, "mixed")
