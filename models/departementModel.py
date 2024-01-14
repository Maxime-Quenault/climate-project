from pydantic import BaseModel, Field
from typing import List
from models.stationModel import Station


class Departement(BaseModel):
    num_departement: str = Field(default="")
    nom_departement: str = Field(default="")
    stations: List[Station]
    avg_latitude: float = Field(default=0.0)
    avg_longitude: float = Field(default=0.0)
