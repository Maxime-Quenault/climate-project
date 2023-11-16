from pydantic import BaseModel
from typing import List

class Station(BaseModel):
    code_station: str
    nom_station: str
    latitude: float
    longitude: float