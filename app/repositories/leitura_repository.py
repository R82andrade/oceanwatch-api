from datetime import datetime

from sqlalchemy.orm import Session

from app.models.leitura import Leitura
from app.schemas.leitura import LeituraCreate


class LeituraRepository:

    def criar_leitura(
        self,
        db: Session,
        leitura: LeituraCreate
    ):
        nova_leitura = Leitura(
            boia_id=leitura.boia_id,
            temperatura_agua=leitura.temperatura_agua,
            altura_onda=leitura.altura_onda,
            velocidade_vento=leitura.velocidade_vento,
            data_hora=datetime.now(),
        )

        db.add(nova_leitura)
        db.commit()
        db.refresh(nova_leitura)

        return nova_leitura

    def listar_leituras(self, db: Session):
        return db.query(Leitura).all()

    def listar_leituras_por_boia(
        self,
        db: Session,
        boia_id: int
    ):
        return (
            db.query(Leitura)
            .filter(Leitura.boia_id == boia_id)
            .all()
        )

    def atualizar_leitura(
        self,
        db: Session,
        leitura_id: int,
        dados: LeituraCreate
    ):
        leitura = (
            db.query(Leitura)
            .filter(Leitura.id == leitura_id)
            .first()
        )

        if leitura is None:
            return None

        leitura.temperatura_agua = dados.temperatura_agua
        leitura.altura_onda = dados.altura_onda
        leitura.velocidade_vento = dados.velocidade_vento

        db.commit()
        db.refresh(leitura)

        return leitura
