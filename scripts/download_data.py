"""Download official public Jeff Sackmann ATP/WTA match CSVs."""
from __future__ import annotations

import argparse
import csv
import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://raw.githubusercontent.com/JeffSackmann/{tour_repo}/master/{filename}"
TOURS = {"atp": "tennis_atp", "wta": "tennis_wta"}
REQUIRED = {"tourney_date", "winner_name", "loser_name", "surface"}

def download_file(tour: str, year: int, output_dir: Path) -> Path:
    if tour not in TOURS:
        raise ValueError("tour must be 'atp' or 'wta'")
    filename = f"{tour}_matches_{year}.csv"
    url = BASE.format(tour_repo=TOURS[tour], filename=filename)
    request = urllib.request.Request(url, headers={"User-Agent": "AO-Predictor-2027/0.1"})
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"Download failed for {url}: HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Could not reach data source {url}: {exc.reason}") from exc

    text = raw.decode("utf-8-sig")
    reader = csv.DictReader(text.splitlines())
    if not reader.fieldnames or not REQUIRED.issubset(set(reader.fieldnames)):
        raise ValueError(f"{filename} does not contain the expected match columns")
    if not any(True for _ in reader):
        raise ValueError(f"{filename} contains no match rows; refusing to save an empty dataset")

    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / filename
    temporary = destination.with_suffix(".csv.part")
    temporary.write_bytes(raw)
    temporary.replace(destination)

    manifest_path = output_dir / "download_manifest.json"
    manifest = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest[filename] = {
        "source": url,
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
        "bytes": len(raw),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return destination

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tour", choices=TOURS, required=True)
    parser.add_argument("--years", nargs="+", type=int, required=True)
    parser.add_argument("--output", type=Path, default=Path("data/raw"))
    args = parser.parse_args()
    for year in args.years:
        path = download_file(args.tour, year, args.output)
        print(f"Saved {path}")

if __name__ == "__main__":
    main()
