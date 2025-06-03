from collections import defaultdict
from typing import Any, DefaultDict, Dict, List, Set

import httpx


def fetch_and_inspect_operation_pc(
    n: int = 10, timeout: int = 60, **params: Any
) -> None:
    url = "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/operation_pc"
    params["size"] = n
    # Try adding a filter to avoid timeouts. Uncomment and adjust as needed:
    params["date_prelevement_min"] = "2024-01-01"
    # params["code_station"] = "YOUR_KNOWN_STATION_CODE"

    try:
        resp = httpx.get(url, params=params, timeout=timeout)
        resp.raise_for_status()
        data: List[Dict[str, Any]] = resp.json().get("data", [])
    except Exception as e:
        print(f"ERROR: {e}")
        return

    type_map: DefaultDict[str, Set[str]] = defaultdict(set)
    example_map: Dict[str, Any] = {}

    for item in data:
        for k, v in item.items():
            type_map[k].add(type(v).__name__)
            if k not in example_map:
                example_map[k] = v

    print("Field types and examples from API response:")
    for k in sorted(type_map):
        types = ", ".join(sorted(type_map[k]))
        example = repr(example_map[k])
        print(f"{k:35} {types:15}   example: {example}")


if __name__ == "__main__":
    fetch_and_inspect_operation_pc(n=1, timeout=60)
