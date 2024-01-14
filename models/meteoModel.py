from pydantic import BaseModel, Field
from typing import List
from datetime import date
from models.departementModel import Departement
from models.infometeoModel import InfoMeteo

class Meteo(BaseModel):
    departement: str = Field(default="")
    date: str = Field(default="")
    matin: InfoMeteo
    apremidi: InfoMeteo

    def to_dict(self):
        return {
            "departement": self.departement,
            "date": self.date,
            "matin": self.matin.to_dict(),
            "apremidi": self.apremidi.to_dict()
        }
    