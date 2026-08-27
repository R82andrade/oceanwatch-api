from datetime import datetime

from pydantic import BaseModel, Field


class LeituraCreate(BaseModel):
    boia_id: int
    temperatura_agua: float = Field(..., ge=0)
    altura_onda: float = Field(..., ge=0)
    velocidade_vento: float = Field(..., ge=0)
