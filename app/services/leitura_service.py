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

    def deletar_leitura(
        self,
        db: Session,
        leitura_id: int
    ):
        return self.repository.deletar_leitura(
            db,
            leitura_id
        )

    def buscar_leitura_por_id(
        self,
        db: Session,
        leitura_id: int
    ):
        return self.repository.buscar_leitura_por_id(
            db,
            leitura_id
        )

    def calcular_temperatura_media(
        self,
        db: Session,
        boia_id: int
    ):
        return self.repository.calcular_temperatura_media(
            db,
            boia_id
        )

    def gerar_resumo_boia(
        self,
        db: Session,
        boia_id: int
    ):
        return self.repository.gerar_resumo_boia(
            db,
            boia_id
        )

    def analisar_risco(
        self,
        db: Session,
        leitura_id: int
    ):
        return self.repository.analisar_risco(
            db,
            leitura_id
        )

    def buscar_ultima_leitura_da_boia(
        self,
        db: Session,
        boia_id: int
    ):
        return self.repository.buscar_ultima_leitura_da_boia(
            db,
            boia_id
        )

    def buscar_historico_risco(
        self,
        db: Session,
        boia_id: int
    ):
        return self.repository.buscar_historico_risco(
            db,
            boia_id
        )

    def analisar_tendencia(
        self,
        db: Session,
        boia_id: int
    ):
        return self.repository.analisar_tendencia(
            db,
            boia_id
        )

    def gerar_dashboard_boia(
        self,
        db: Session,
        boia_id: int
    ):
        return self.repository.gerar_dashboard_boia(
            db,
            boia_id
        )

    def gerar_painel_boia(
        self,
        db: Session,
        boia_id: int
    ):
        dashboard = self.repository.gerar_dashboard_boia(
            db,
            boia_id
        )

        if dashboard is None:
            return None

        tendencia = self.repository.analisar_tendencia(
            db,
            boia_id
        )

        historico = self.repository.buscar_historico_risco(
            db,
            boia_id
        )

        dashboard["temperatura_media"] = round(
            dashboard["temperatura_media"], 2
        )

        dashboard["altura_onda_media"] = round(
            dashboard["altura_onda_media"], 2
        )

        dashboard["vento_medio"] = round(
            dashboard["vento_medio"], 2
        )

        return {
            "dashboard": dashboard,
            "tendencia": tendencia,
            "historico_risco": historico
        }
