from pydantic import BaseModel, Field
from typing import List

class Station(BaseModel):
    code_station: str = Field(default="")
    nom_station: str = Field(default="")
    latitude: float
    longitude: float

    def to_dict(self):
        return {
            "code_station": self.code_station,
            "nom_station": self.nom_station,
            "latitude": self.latitude,
            "longitude": self.longitude
        }