from pydantic import BaseModel
from typing import List

from stationModel import Station


class Departement(BaseModel):
    departement: str
    nom_departement: str
    list_stations: List[Station]
    avg_latitude: float
    avg_longitude: float
