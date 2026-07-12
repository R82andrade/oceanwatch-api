from sqlalchemy.orm import Session

from app.models.boia import Boia
from app.schemas.boia import BoiaCreate


class BoiaRepository:

    def criar_boia(self, db: Session, boia: BoiaCreate):

        nova_boia = Boia(
            nome=boia.nome,
            numero_serie=boia.numero_serie,
            latitude=boia.latitude,
            longitude=boia.longitude,
        )

        db.add(nova_boia)
        db.commit()
        db.refresh(nova_boia)

        return nova_boia