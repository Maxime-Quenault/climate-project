from pydantic import BaseModel
from typing import List
from datetime import date
from models.departementModel import Departement
from models.infometeoModel import InfoMeteo

class Meteo(BaseModel):
    departement: Departement
    date: date
    matin: InfoMeteo
    apremidi: InfoMeteo
    