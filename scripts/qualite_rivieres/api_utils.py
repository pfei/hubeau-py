import logging
from typing import List

import httpx

from hubeau_py.models.qualite_rivieres import AnalysePc, StationPc

logger = logging.getLogger(__name__)

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


def fetch_analyses(station_code: str, batch_size: int = 1000) -> List[AnalysePc]:
    """Fetch ALL analyses for a station with pagination handling."""
    url = ENDPOINTS["analyse_pc"]
    analyses = []
    start = 0

    while True:
        try:
            resp = httpx.get(
                url,
                params={
                    "code_station": station_code,
                    "size": batch_size,
                    "start": start,
                },
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json().get("data", [])

            if not data:  # No more results
                break

            analyses.extend([AnalysePc(**item) for item in data])
            start += batch_size

            # Break if we get fewer results than requested
            if len(data) < batch_size:
                break

        except Exception as e:
            logger.error(f"Error fetching analyses for station {station_code}: {e}")
            break

    return analyses
