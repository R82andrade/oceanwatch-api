from pydantic import BaseModel


class BoiaCreate(BaseModel):
    nome: str
    codigo: str
    latitude: float
    longitude: float

from pydantic import BaseModel


class BoiaCreate(BaseModel):
    nome: str
    numero_serie: str
    latitude: float
    longitude: float