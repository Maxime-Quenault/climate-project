from pydantic import BaseModel, Field
from typing import List
from datetime import date
from models.departementModel import Departement
from models.infometeoModel import InfoMeteo

class Conditions(BaseModel):
    temperature_min: int = Field(default=0)
    humidity_max: int = Field(default=0)
    wind_speed_max: int = Field(default=999)
    rainfall_max: int = Field(default=999)

    def to_dict(self):
        return {
            "temperature_min": self.temperature_min,
            "humidity_max": self.humidity_max,
            "wind_speed_max": self.wind_speed_max,
            "rainfall_max": self.rainfall_max
        }
    