from typing import List

import httpx

from hubeau_py.models.qualite_rivieres import StationPC


class QualiteRivieresAPI:
    BASE_URL = "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres"

    def get_stations(self, commune: str) -> List[StationPC]:
        url = f"{self.BASE_URL}/station_pc"
        params = {"libelle_commune": commune}
        resp = httpx.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json().get("data", [])
        return [StationPC(**item) for item in data]
