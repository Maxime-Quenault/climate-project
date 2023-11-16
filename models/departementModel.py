from pydantic import BaseModel
from typing import List
from models.stationModel import Station


class Departement(BaseModel):
    num_departement: str
    nom_departement: str
    stations: List[Station]
    avg_latitude: float
    avg_longitude: float
