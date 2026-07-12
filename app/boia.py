from fastapi import APIRouter, Depends
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
    return service.criar_boia(db, boia)