from sqlalchemy.orm import Session

from app.repositories.boia_repository import BoiaRepository
from app.schemas.boia import BoiaCreate


class BoiaService:

    def __init__(self):
        self.repository = BoiaRepository()

    def criar_boia(self, db: Session, boia: BoiaCreate):
        return self.repository.criar_boia(db, boia)

    def listar_boias(self, db: Session):
        return self.repository.listar_boias(db)

    def buscar_boia_por_id(self, db: Session, boia_id: int):
        return self.repository.buscar_boia_por_id(db, boia_id)

