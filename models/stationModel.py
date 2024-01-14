from pydantic import BaseModel, Field
from typing import List

class Station(BaseModel):
    code_station: str = Field(default="")
    nom_station: str = Field(default="")
    latitude: float = Field(default=0.0)
    longitude: float = Field(default=0.0)