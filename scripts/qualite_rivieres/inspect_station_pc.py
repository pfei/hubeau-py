from collections import defaultdict
from typing import Any, DefaultDict, Dict, List, Set

import httpx


def fetch_and_inspect_station_pc(n: int = 10, **params: Any) -> None:
    url = "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/station_pc"
    params["size"] = n
    try:
        resp = httpx.get(url, params=params, timeout=60)
        resp.raise_for_status()
        data: List[Dict[str, Any]] = resp.json().get("data", [])
    except Exception as e:
        print(f"ERROR: {e}")
        return

    type_map: DefaultDict[str, Set[str]] = defaultdict(set)
    example_map: Dict[str, Any] = {}

    print("Sample station codes:")
    for item in data:
        code = item.get("code_station")
        libelle = item.get("libelle_station")
        print(f"  code_station: {code} | libelle_station: {libelle}")

    for item in data:
        for k, v in item.items():
            type_map[k].add(type(v).__name__)
            if k not in example_map:
                example_map[k] = v

    print("\nField types and examples from API response:")
    for k in sorted(type_map):
        types = ", ".join(sorted(type_map[k]))
        example = repr(example_map[k])
        print(f"{k:35} {types:15}   example: {example}")


if __name__ == "__main__":
    fetch_and_inspect_station_pc(n=5)
