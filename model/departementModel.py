from pydantic import BaseModel
from typing import List

from stationModel import Station


class Departement(BaseModel):
    numero: str
    nom: str
    list_stations: List[Station]