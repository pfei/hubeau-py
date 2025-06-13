"""Inspect fields available in Hubeau Hydrométrie API responses.

Usage:
    poetry run python scripts/hydrometrie/inspect_fields.py referentiel/sites
    poetry run python scripts/hydrometrie/inspect_fields.py referentiel/stations
    poetry run python scripts/hydrometrie/inspect_fields.py observations_tr
    poetry run python scripts/hydrometrie/inspect_fields.py obs_elab

Prints all unique field names found in the response for the given endpoint.
"""

import sys
from typing import Any, Dict, List, Optional, Set, Union

import httpx

BASE_URL = "https://hubeau.eaufrance.fr/api/v2/hydrometrie"


def get_field_info(
    endpoint: str, sample_size: int = 10
) -> Dict[str, Dict[str, Union[Set[type], Optional[Set[Any]], List[Any]]]]:
    url = f"{BASE_URL}/{endpoint}"
    resp = httpx.get(url, params={"size": sample_size})
    resp.raise_for_status()
    data: List[Dict[str, Any]] = resp.json()["data"]
    field_info: Dict[
        str, Dict[str, Union[Set[type], Optional[Set[Any]], List[Any]]]
    ] = {}

    for record in data:
        for key, value in record.items():
            if key not in field_info:
                field_info[key] = {"types": set(), "values": []}
            field_info[key]["types"].add(type(value))  # type: ignore[union-attr]
            field_info[key]["values"].append(value)  # type: ignore[union-attr]

    for key in field_info:
        try:
            unique_values: Optional[Set[Any]] = set(field_info[key]["values"])  # type: ignore[arg-type]
            field_info[key]["unique_values"] = unique_values
        except TypeError:
            field_info[key]["unique_values"] = None

    return field_info


def suggest_pydantic_type(types: Set[type], unique_values: Optional[Set[Any]]) -> str:
    type_names = {t.__name__ for t in types}
    if "NoneType" in type_names:
        optional = True
        type_names.discard("NoneType")
    else:
        optional = False

    if not type_names:
        return "None = None"

    if len(type_names) == 1:
        py_type = type_names.pop()
        if py_type == "list":
            if unique_values and all(
                isinstance(x, (str, type(None))) for x in unique_values if x is not None
            ):
                py_type = "List[str]"
            else:
                py_type = "List[Any]"
    else:
        py_type = " | ".join(sorted(type_names))

    if optional:
        return f"Optional[{py_type}] = None"
    else:
        return py_type


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python inspect.py <endpoint>")
        sys.exit(1)
    endpoint = sys.argv[1]
    field_info = get_field_info(endpoint)

    print(f"\nField info for {endpoint}:\n")
    for field, info in sorted(field_info.items()):
        types_str = ", ".join(t.__name__ for t in info["types"])  # type: ignore[union-attr]
        unique_values = info["unique_values"]
        if unique_values is not None:
            try:
                sample_values = sorted(unique_values)[:5]
            except TypeError:
                sample_values = list(unique_values)[:5]
        else:
            sample_values = ["(unhashable, e.g., dict or list of dicts)"]
        pydantic_type = suggest_pydantic_type(
            info["types"],  # type: ignore[arg-type]
            unique_values,  # type: ignore[arg-type]
        )
        print(f"{field}:")
        print(f"  types: {types_str}")
        print(f"  sample values: {sample_values}")
        print(f"  suggested Pydantic type: {pydantic_type}")
        print()

    # Print Pydantic model template
    print("\n===== Pydantic Model Template =====")
    print("from typing import Optional, List, Any")
    print("from pydantic import BaseModel")
    print("\nclass YourModel(BaseModel):")
    for field, info in sorted(field_info.items()):
        pydantic_type = suggest_pydantic_type(
            info["types"],  # type: ignore[arg-type]
            info["unique_values"],  # type: ignore[arg-type]
        )
        # Handle fields that are always None (unlikely in practice, but possible)
        if pydantic_type == "None = None":
            print(f"    {field}: None = None")
        else:
            print(f"    {field}: {pydantic_type}")


if __name__ == "__main__":
    main()
