from pydantic import BaseModel
from typing import List
from datetime import date

class InfoMeteo(BaseModel):
    temperature: float
    pression: float
    humidite: float
    point_de_rose : float
    vent_moyen: float
    vent_rafales: float
    vent_direction: float
    pluie_1h : float
    pluie_3h : float