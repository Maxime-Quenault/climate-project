from pydantic import BaseModel
from typing import List
from datetime import date

class InfoMeteo(BaseModel):
    temperature: int
    pression: int
    humidite: int
    vent_moyen: int
    vent_rafales: int
    vent_direction: int
    nebulosite: int