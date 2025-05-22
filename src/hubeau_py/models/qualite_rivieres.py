from pydantic import BaseModel


class StationPC(BaseModel):
    code_station: str
    libelle_commune: str
