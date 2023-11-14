from pydantic import BaseModel
from typing import List

class Station(BaseModel):
    code: str
    nom: str
    longitude: str
    lattitude: str