from sqlalchemy.orm import Session

from app.repositories.boia_repository import BoiaRepository
from app.schemas.boia import BoiaCreate


class BoiaService:

    def __init__(self):
        self.repository = BoiaRepository()

    def criar_boia(self, db: Session, boia: BoiaCreate):
        return self.repository.criar_boia(db, boia)

