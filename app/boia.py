from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.boia import BoiaCreate
from app.services.boia_service import BoiaService

router = APIRouter(tags=["boias"])

service = BoiaService()


@router.post("/boias")
def criar_boia(
    boia: BoiaCreate,
    db: Session = Depends(get_db)
):
    try:
        return service.criar_boia(db, boia)
    except ValueError as exc:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "mensagem": "Não foi possível cadastrar a boia.",
                "erro": str(exc),
            },
        )
    except IntegrityError as exc:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "mensagem": "Não foi possível cadastrar a boia.",
                "erro": "Já existe uma boia com este número de série.",
            },
        )


@router.get("/boias")
def listar_boias(db: Session = Depends(get_db)):
    return service.listar_boias(db)


@router.get("/boias/{boia_id}")
def buscar_boia(boia_id: int, db: Session = Depends(get_db)):
    return service.buscar_boia_por_id(db, boia_id)
