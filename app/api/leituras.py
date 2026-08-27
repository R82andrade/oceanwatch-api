from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.leitura import LeituraCreate
from app.services.leitura_service import LeituraService


router = APIRouter(
    prefix="/leituras",
    tags=["Leituras"]
)

boias_router = APIRouter(
    prefix="/boias",
    tags=["Leituras das Boias"]
)

service = LeituraService()


@router.post("/")
def criar_leitura(
    leitura: LeituraCreate,
    db: Session = Depends(get_db)
):
    return service.criar_leitura(
        db,
        leitura
    )


@router.get("/")
def listar_leituras(
    db: Session = Depends(get_db)
):
    return service.listar_leituras(db)


@boias_router.get("/{boia_id}/leituras")
def listar_leituras_por_boia(
    boia_id: int,
    db: Session = Depends(get_db)
):
    return service.listar_leituras_por_boia(
        db,
        boia_id
    )


@router.put("/{leitura_id}")
def atualizar_leitura(
    leitura_id: int,
    dados: LeituraCreate,
    db: Session = Depends(get_db)
):
    leitura = service.atualizar_leitura(
        db,
        leitura_id,
        dados
    )

    if leitura is None:
        raise HTTPException(
            status_code=404,
            detail="Leitura não encontrada."
        )

    return leitura
