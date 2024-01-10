from pydantic import BaseModel
from typing import List
from datetime import date
from models.departementModel import Departement
from models.infometeoModel import InfoMeteo

class Meteo(BaseModel):
    departement: str
    date: str
    matin: InfoMeteo
    apremidi: InfoMeteo
    