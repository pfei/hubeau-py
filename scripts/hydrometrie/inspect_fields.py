"""Inspect fields available in Hubeau Hydrométrie API responses.

Usage:
    poetry run python scripts/hydrometrie/inspect_fields.py referentiel/sites
    poetry run python scripts/hydrometrie/inspect_fields.py referentiel/stations
    poetry run python scripts/hydrometrie/inspect_fields.py observations_tr
    poetry run python scripts/hydrometrie/inspect_fields.py obs_elab

Prints all unique field names found in the response for the given endpoint.
"""

import sys
from typing import Set

import httpx

BASE_URL = "https://hubeau.eaufrance.fr/api/v2/hydrometrie"


def get_fields(endpoint: str, sample_size: int = 10) -> Set[str]:
    url = f"{BASE_URL}/{endpoint}"
    resp = httpx.get(url, params={"size": sample_size})
    resp.raise_for_status()
    data = resp.json()["data"]
    fields = set()
    for record in data:
        fields.update(record.keys())
    return fields


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python inspect.py <endpoint>")
        sys.exit(1)
    endpoint = sys.argv[1]
    fields = get_fields(endpoint)
    print(f"Fields for {endpoint}:")
    print("\n".join(sorted(fields)))


if __name__ == "__main__":
    main()
