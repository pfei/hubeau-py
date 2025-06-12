import json
from pathlib import Path
from typing import Any, Dict, List, Optional, cast

import httpx
from tqdm import tqdm

BASE_URL = "https://hubeau.eaufrance.fr/api/v2/hydrometrie"
OUTPUT_DIR = Path("data/exploration/hydrometrie")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# List of main endpoints to explore
ENDPOINTS = [
    "referentiel/sites",
    "referentiel/stations",
    "observations_tr",
    "obs_elab",
]


def fetch_sample(endpoint: str, size: int = 10) -> Optional[List[Dict[str, Any]]]:
    """Fetch sample data from a Hydrometrie endpoint."""
    url = f"{BASE_URL}/{endpoint}"
    try:
        resp = httpx.get(url, params={"size": size})
        resp.raise_for_status()
        data = resp.json().get("data", [])
        if not isinstance(data, list):
            data = []
        return cast(List[Dict[str, Any]], data)
    except Exception as e:
        print(f"Error fetching {endpoint}: {e}")
        return None


def get_fields(records: List[Dict[str, Any]]) -> List[str]:
    """Extract unique field names from a list of records."""
    if not records:
        return []
    fields: set[str] = set()
    for rec in records:
        fields.update(rec.keys())
    return sorted(fields)


def explore_endpoints() -> None:
    """Explore all Hydrometrie endpoints and save results."""
    results = {}
    for endpoint in tqdm(ENDPOINTS, desc="Exploring endpoints"):
        sample = fetch_sample(endpoint)
        if sample is None:
            continue
        fields = get_fields(sample)
        results[endpoint] = {
            "sample": sample,
            "fields": fields,
        }
        # Save sample and fields for each endpoint
        with open(OUTPUT_DIR / f"{endpoint.replace('/', '_')}_sample.json", "w") as f:
            json.dump(sample, f, indent=2)
        with open(OUTPUT_DIR / f"{endpoint.replace('/', '_')}_fields.txt", "w") as f:
            f.write("\n".join(fields))
        print(f"\nEndpoint: {endpoint}")
        print(f"Fields: {', '.join(fields)}")
    # Save combined results
    with open(OUTPUT_DIR / "explore_results.json", "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    explore_endpoints()
