from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories.boia_repository import BoiaRepository
from app.repositories.leitura_repository import LeituraRepository
from app.schemas.leitura import LeituraCreate


class LeituraService:

    def __init__(self):
        self.boia_repository = BoiaRepository()
        self.repository = LeituraRepository()

    def criar_leitura(
        self,
        db: Session,
        leitura: LeituraCreate
    ):
        boia = self.boia_repository.buscar_boia_por_id(db, leitura.boia_id)

        if boia is None:
            raise HTTPException(
                status_code=404,
                detail="Boia não encontrada.",
            )

        return self.repository.criar_leitura(
            db,
            leitura
        )

    def listar_leituras(self, db: Session):

        return self.repository.listar_leituras(db)

    def listar_leituras_por_boia(
        self,
        db: Session,
        boia_id: int
    ):
        return self.repository.listar_leituras_por_boia(
            db,
            boia_id
        )

    def atualizar_leitura(
        self,
        db: Session,
        leitura_id: int,
        dados: LeituraCreate
    ):
        return self.repository.atualizar_leitura(
            db,
            leitura_id,
            dados
        )
