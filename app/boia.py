from fastapi import APIRouter, Depends, HTTPException, status
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
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc