from pydantic import BaseModel


class BoiaCreate(BaseModel):
    nome: str
    numero_serie: str
    latitude: float
    longitude: float


class BoiaUpdate(BaseModel):
    nome: str
    numero_serie: str
    latitude: float
    longitude: float
