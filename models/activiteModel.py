from pydantic import BaseModel, Field
from models.conditionsModel import Conditions


class Activite(BaseModel):
    name: str = Field(default="")
    departement: str = Field(default="")
    longitude: float
    latitude: float
    type: str = Field(default="")
    conditions: Conditions

    def to_dict(self):
        return {
            "name": self.name,
            "departement": self.departement,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "type": self.type,
            "conditions": self.conditions.to_dict()
        }
    