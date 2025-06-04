# scripts/qualite_rivieres/api_utils.py

from typing import List, Optional

import httpx

from hubeau_py.models.qualite_rivieres import AnalysePc, StationPc

ENDPOINTS = {
    "station_pc": "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/station_pc",
    "analyse_pc": "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/analyse_pc",
}


def fetch_stations(size: int = 10) -> List[StationPc]:
    """Fetch a sample of stations."""
    url = ENDPOINTS["station_pc"]
    resp = httpx.get(url, params={"size": size}, timeout=60)
    resp.raise_for_status()
    data = resp.json().get("data", [])
    return [StationPc(**station) for station in data]


def fetch_analyses(code_station: Optional[str], size: int = 10) -> List[AnalysePc]:
    """Fetch analyses for a station, up to size."""
    if code_station is None:
        return []
    url = ENDPOINTS["analyse_pc"]
    resp = httpx.get(
        url, params={"code_station": code_station, "size": size}, timeout=60
    )
    resp.raise_for_status()
    data = resp.json().get("data", [])
    return [AnalysePc(**analysis) for analysis in data]
