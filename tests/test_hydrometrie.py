import httpx

from hubeau_py.models.hydrometrie import Station


def test_station_model_validation() -> None:
    url = "https://hubeau.eaufrance.fr/api/v2/hydrometrie/referentiel/stations"
    params: dict[str, str | int] = {"code_commune_station": "75056", "size": 1}
    resp = httpx.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()["data"]
    for item in data:
        Station(**item)
