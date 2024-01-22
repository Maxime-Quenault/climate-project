from pydantic import BaseModel, Field
from typing import List
from models.stationModel import Station


class Departement(BaseModel):
    num_departement: str = Field(default="")
    nom_departement: str = Field(default="")
    stations: List[Station]
    avg_latitude: float = Field(default=0.0)
    avg_longitude: float = Field(default=0.0)

    def to_dict(self):
        return {
            "num_departement": self.num_departement,
            "nom_departement": self.nom_departement,
            "stations": [station.to_dict() for station in self.stations],
            "avg_latitude": self.avg_latitude,
            "avg_longitude": self.avg_longitude
        }
