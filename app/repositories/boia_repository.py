from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.boia import Boia
from app.schemas.boia import BoiaCreate, BoiaUpdate


class BoiaRepository:

    def criar_boia(self, db: Session, boia: BoiaCreate):
        nova_boia = Boia(
            nome=boia.nome,
            numero_serie=boia.numero_serie,
            latitude=boia.latitude,
            longitude=boia.longitude,
        )

        db.add(nova_boia)

        try:
            db.commit()
            db.refresh(nova_boia)
            return nova_boia
        except IntegrityError:
            db.rollback()
            raise ValueError("Já existe uma boia com este número de série.")

    def listar_boias(self, db: Session):
        return db.query(Boia).all()

    def buscar_boia_por_id(self, db: Session, boia_id: int):
        return db.query(Boia).filter(Boia.id == boia_id).first()

    def atualizar_boia(
        self,
        db: Session,
        boia_id: int,
        dados: BoiaUpdate,
    ):
        boia = db.query(Boia).filter(Boia.id == boia_id).first()

        if boia is None:
            return None

        boia.nome = dados.nome
        boia.numero_serie = dados.numero_serie
        boia.latitude = dados.latitude
        boia.longitude = dados.longitude

        db.commit()
        db.refresh(boia)

        return boia

    def excluir_boia(self, db: Session, boia_id: int):
        boia = db.query(Boia).filter(Boia.id == boia_id).first()

        if boia is None:
            return None

        db.delete(boia)
        db.commit()

        return boia
