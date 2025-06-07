import json
import logging
import signal
import sys
import time
from datetime import datetime
from multiprocessing import Pool
from pathlib import Path
from typing import Any, Dict, List

import httpx
import pandas as pd
from tqdm import tqdm

from hubeau_py.models.qualite_rivieres import AnalysePc, StationPc
from scripts.qualite_rivieres.api_utils import fetch_analyses

OUTPUT_DIR: Path = Path("data/exploration/qualite_rivieres")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


log_file = OUTPUT_DIR / "station_tsa.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_file, mode="a"),
    ],
)

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


def flush_logs_on_exit(signum, frame) -> None:  # type: ignore[no-untyped-def]
    logging.shutdown()
    sys.exit(0)


signal.signal(signal.SIGINT, flush_logs_on_exit)


def analyze_station_tsa(station: StationPc) -> Dict[str, Any]:
    """Analyze time series feasibility for a station."""
    try:
        logging.info(
            f"Processing station: {station.libelle_station or 'unknown'} "
            f"(code: {station.code_station or 'unknown'})"
        )
        if station.code_station is None:
            return {"station": station.code_station, "tsa_candidates": []}
        analyses: List[AnalysePc] = fetch_analyses(station.code_station, 1000)
        if not analyses:
            return {"station": station.code_station, "tsa_candidates": []}
        param_data: Dict[str, List[AnalysePc]] = {}
        for a in analyses:
            if a.libelle_parametre is None:
                continue
            # Skip analyses with zero or missing resultat
            if getattr(a, "resultat", None) in (None, 0, "0", ""):
                continue
            if a.libelle_parametre not in param_data:
                param_data[a.libelle_parametre] = []
            param_data[a.libelle_parametre].append(a)
        tsa_candidates: List[Dict[str, Any]] = []
        for param, records in param_data.items():
            dates: List[datetime] = []
            for r in records:
                if r.date_prelevement is not None:
                    try:
                        dates.append(datetime.strptime(r.date_prelevement, "%Y-%m-%d"))
                    except ValueError:
                        continue
            if not dates:
                continue
            min_date: datetime = min(dates)
            max_date: datetime = max(dates)
            n_measurements: int = len(dates)
            tsa_candidates.append(
                {
                    "parameter": param,
                    "n_measurements": n_measurements,
                    "min_date": min_date.isoformat(),
                    "max_date": max_date.isoformat(),
                    "time_span_days": (max_date - min_date).days,
                }
            )
        return {
            "station": station.code_station,
            "tsa_candidates": tsa_candidates,
        }
    except Exception as e:
        logging.error(
            f"Error processing station {station.code_station or 'unknown'}: {e}"
        )
        return {"station": station.code_station, "tsa_candidates": [], "error": str(e)}


def save_report(results: List[Dict[str, Any]], output_dir: Path) -> None:
    """Save results as JSON and generate a markdown report."""
    with open(output_dir / "tsa_analysis.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    rows: List[Dict[str, Any]] = []
    for res in results:
        for cand in res["tsa_candidates"]:
            rows.append(
                {
                    "station": res["station"],
                    "parameter": cand["parameter"],
                    "n_measurements": cand["n_measurements"],
                    "min_date": cand["min_date"],
                    "max_date": cand["max_date"],
                    "time_span_days": cand["time_span_days"],
                }
            )
    df: pd.DataFrame = pd.DataFrame(rows)
    # Use semicolon as delimiter to avoid issues with commas in parameter names
    df.to_csv(output_dir / "tsa_analysis.csv", sep=";", index=False)

    try:
        from tabulate import tabulate  # noqa: F401  # type: ignore[import-untyped]
    except ImportError:
        raise RuntimeError(
            "The 'tabulate' package is required for markdown reporting. "
            "Install with: poetry add tabulate"
        )

    report = f"""# Hubeau API Time Series Analysis Report

## Summary

- **Stations analyzed:** {len(results)}
- **Parameters with measurements:** {df['parameter'].nunique()}
- **Total measurement series:** {len(df)}

## Best Candidates for Time Series Analysis

{df.sort_values("n_measurements", ascending=False).head(10).to_markdown()}

## Time Span Distribution

{df.groupby("parameter")["time_span_days"].describe().to_markdown()}
"""
    with open(output_dir / "tsa_analysis_report.md", "w", encoding="utf-8") as f:
        f.write(report)


def get_total_station_count() -> int:
    url = "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/station_pc"
    resp = httpx.get(url, params={"size": 1}, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    return int(data["count"])


def fetch_all_stations(total: int, batch_size: int = 1000) -> List[StationPc]:
    """Fetch all stations using pagination."""
    stations: List[StationPc] = []
    url = "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/station_pc"
    for start in tqdm(range(0, total, batch_size), desc="Fetching stations"):
        resp = httpx.get(url, params={"start": start, "size": batch_size}, timeout=60)
        resp.raise_for_status()
        data = resp.json()["data"]
        stations.extend(StationPc(**s) for s in data)
    return stations


def main() -> None:
    start_time = time.time()
    total_stations = get_total_station_count()
    print(f"WARNING: There are {total_stations} stations available in the database.")
    print("Processing all stations may take a long time!\n")
    print("Fetching stations...")
    stations: List[StationPc] = fetch_all_stations(total_stations)
    print("Analyzing stations in parallel...")
    # Use multiprocessing to parallelize station analysis
    with Pool() as pool:  # Defaults to number of available CPU cores[1]
        results = list(
            tqdm(
                pool.imap(analyze_station_tsa, stations),
                total=len(stations),
                desc="Analyzing stations",
            )
        )
    print("Saving report...")
    save_report(results, OUTPUT_DIR)
    elapsed = time.time() - start_time
    print(f"Done in {elapsed:.2f} seconds")


if __name__ == "__main__":

    main()
