from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.boia_repository import BoiaRepository
from app.schemas.boia import BoiaCreate, BoiaUpdate


class BoiaService:

    def __init__(self):
        self.repository = BoiaRepository()

    def criar_boia(self, db: Session, boia: BoiaCreate):
        return self.repository.criar_boia(db, boia)

    def listar_boias(self, db: Session):
        return self.repository.listar_boias(db)

    def buscar_boia_por_id(self, db: Session, boia_id: int):
        boia = self.repository.buscar_boia_por_id(db, boia_id)

        if boia is None:
            raise HTTPException(
                status_code=404,
                detail="Boia não encontrada.",
            )

        return boia

    def atualizar_boia(
        self,
        db: Session,
        boia_id: int,
        dados: BoiaUpdate,
    ):
        return self.repository.atualizar_boia(db, boia_id, dados)

    def excluir_boia(self, db: Session, boia_id: int):
        return self.repository.excluir_boia(db, boia_id)

