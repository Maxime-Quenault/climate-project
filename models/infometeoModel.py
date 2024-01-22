from pydantic import BaseModel, Field
from typing import List
from datetime import date

class InfoMeteo(BaseModel):
    temperature: float = Field(default=999)
    nebulosite: float = Field(default=0.0) 
    pression: float = Field(default=0.0)
    humidite: float = Field(default=999)
    point_de_rose : float = Field(default=0.0)
    vent_moyen: float = Field(default=0.0)
    vent_rafales: float = Field(default=0.0)
    vent_direction: float = Field(default=0.0)
    pluie_1h : float = Field(default=0.0)
    pluie_3h : float = Field(default=0.0)
    neige_au_sol: float = Field(default=0.0)

    def to_dict(self):
        return {
            "temperature": self.temperature,
            "nebulosite": self.nebulosite,
            "pression": self.pression,
            "humidite": self.humidite,
            "point_de_rose": self.point_de_rose,
            "vent_moyen": self.vent_moyen,
            "vent_rafales": self.vent_rafales,
            "vent_direction": self.vent_direction,
            "pluie_1h": self.pluie_1h,
            "pluie_3h": self.pluie_3h,
            "neige_au_sol": self.neige_au_sol
        }