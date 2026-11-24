from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = {"tourney_date", "winner_name", "loser_name", "surface"}

def load_matches(data_dir: str | Path, tour: str = "atp") -> pd.DataFrame:
    """Load annual CSVs; never invent missing match data."""
    paths = sorted(Path(data_dir).glob(f"{tour}_matches_*.csv"))
    if not paths:
        raise FileNotFoundError(f"No {tour.upper()} match CSV files found in {data_dir}. See README for sources.")
    frames = []
    for path in paths:
        frame = pd.read_csv(path, low_memory=False)
        missing = REQUIRED_COLUMNS.difference(frame.columns)
        if missing:
            raise ValueError(f"{path.name} missing columns: {sorted(missing)}")
        frame["tourney_date"] = pd.to_datetime(frame["tourney_date"].astype(str), format="%Y%m%d", errors="coerce")
        frame["source_file"] = path.name
        frames.append(frame)
    data = pd.concat(frames, ignore_index=True).dropna(subset=["tourney_date", "winner_name", "loser_name"])
    return data.sort_values("tourney_date").reset_index(drop=True)
