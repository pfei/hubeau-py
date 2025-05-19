import httpx
from pydantic import BaseModel


class StationPC(BaseModel):
    code_station: str
    libelle_commune: str


class HubeauClient:
    BASE_URL = "https://hubeau.eaufrance.fr/api/v2"

    def get_stations(self, commune: str) -> list[StationPC]:
        url = f"{self.BASE_URL}/qualite_rivieres/station_pc"
        params = {"libelle_commune": commune}
        resp = httpx.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json().get("data", [])
        return [StationPC(**item) for item in data]
