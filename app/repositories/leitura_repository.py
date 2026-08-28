from datetime import datetime

from sqlalchemy.orm import Session

from app.models.leitura import Leitura
from app.schemas.leitura import LeituraCreate
from app.services.risk_analyzer import RiskAnalyzer


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

    def deletar_leitura(
        self,
        db: Session,
        leitura_id: int
    ):
        leitura = (
            db.query(Leitura)
            .filter(Leitura.id == leitura_id)
            .first()
        )

        if leitura is None:
            return None

        db.delete(leitura)
        db.commit()

        return leitura

    def buscar_leitura_por_id(
        self,
        db: Session,
        leitura_id: int
    ):
        return (
            db.query(Leitura)
            .filter(Leitura.id == leitura_id)
            .first()
        )

    def calcular_temperatura_media(
        self,
        db: Session,
        boia_id: int
    ):
        leituras = (
            db.query(Leitura)
            .filter(Leitura.boia_id == boia_id)
            .all()
        )

        if not leituras:
            return None

        temperatura_media = sum(
            leitura.temperatura_agua
            for leitura in leituras
        ) / len(leituras)

        return temperatura_media

    def gerar_resumo_boia(
        self,
        db: Session,
        boia_id: int
    ):
        leituras = (
            db.query(Leitura)
            .filter(Leitura.boia_id == boia_id)
            .all()
        )

        if not leituras:
            return None

        temperaturas = [
            leitura.temperatura_agua
            for leitura in leituras
        ]

        ondas = [
            leitura.altura_onda
            for leitura in leituras
        ]

        ventos = [
            leitura.velocidade_vento
            for leitura in leituras
        ]

        return {
            "total_leituras": len(leituras),
            "temperatura_media": sum(temperaturas) / len(temperaturas),
            "altura_onda_media": sum(ondas) / len(ondas),
            "maior_onda": max(ondas),
            "vento_medio": sum(ventos) / len(ventos),
            "maior_vento": max(ventos)
        }

    def analisar_risco(
        self,
        db: Session,
        leitura_id: int
    ):
        leitura = (
            db.query(Leitura)
            .filter(Leitura.id == leitura_id)
            .first()
        )

        if leitura is None:
            return None

        nivel = RiskAnalyzer.analisar(
            leitura.altura_onda,
            leitura.velocidade_vento
        )

        return {
            "leitura_id": leitura.id,
            "boia_id": leitura.boia_id,
            "nivel": nivel,
            "mensagem": (
                "Condições marítimas severas. "
                "Recomenda-se atenção imediata."
                if nivel == "RISCO"
                else
                "Condições que exigem monitoramento."
                if nivel == "ATENCAO"
                else
                "Condições normais."
            ),
            "altura_onda": leitura.altura_onda,
            "velocidade_vento": leitura.velocidade_vento
        }

    def buscar_ultima_leitura_da_boia(
        self,
        db: Session,
        boia_id: int
    ):
        return (
            db.query(Leitura)
            .filter(Leitura.boia_id == boia_id)
            .order_by(Leitura.data_hora.desc())
            .first()
        )

    def buscar_historico_risco(
        self,
        db: Session,
        boia_id: int
    ):
        leituras = (
            db.query(Leitura)
            .filter(Leitura.boia_id == boia_id)
            .order_by(Leitura.data_hora.asc())
            .all()
        )

        historico = []

        for leitura in leituras:
            nivel = RiskAnalyzer.analisar(
                leitura.altura_onda,
                leitura.velocidade_vento
            )

            historico.append({
                "leitura_id": leitura.id,
                "data_hora": leitura.data_hora,
                "nivel": nivel
            })

        return historico

    def analisar_tendencia(
        self,
        db: Session,
        boia_id: int
    ):
        leituras = (
            db.query(Leitura)
            .filter(Leitura.boia_id == boia_id)
            .order_by(Leitura.data_hora.desc())
            .limit(2)
            .all()
        )

        if len(leituras) < 2:
            return None

        niveis = []

        for leitura in leituras:
            nivel = RiskAnalyzer.analisar(
                leitura.altura_onda,
                leitura.velocidade_vento
            )

            niveis.append(nivel)

        nivel_atual = niveis[0]
        nivel_anterior = niveis[1]

        ordem = {
            "NORMAL": 1,
            "ATENCAO": 2,
            "RISCO": 3
        }

        if ordem[nivel_atual] > ordem[nivel_anterior]:
            tendencia = "PIORANDO"

        elif ordem[nivel_atual] < ordem[nivel_anterior]:
            tendencia = "MELHORANDO"

        else:
            tendencia = "ESTAVEL"

        return {
            "boia_id": boia_id,
            "nivel_atual": nivel_atual,
            "nivel_anterior": nivel_anterior,
            "tendencia": tendencia
        }

    def gerar_dashboard_boia(
        self,
        db: Session,
        boia_id: int
    ):
        leituras = (
            db.query(Leitura)
            .filter(Leitura.boia_id == boia_id)
            .order_by(Leitura.data_hora.desc())
            .all()
        )

        if not leituras:
            return None

        temperaturas = [
            leitura.temperatura_agua
            for leitura in leituras
        ]

        ondas = [
            leitura.altura_onda
            for leitura in leituras
        ]

        ventos = [
            leitura.velocidade_vento
            for leitura in leituras
        ]

        ultima_leitura = leituras[0]

        nivel_atual = RiskAnalyzer.analisar(
            ultima_leitura.altura_onda,
            ultima_leitura.velocidade_vento
        )

        return {
            "total_leituras": len(leituras),
            "ultima_leitura_id": ultima_leitura.id,
            "nivel_atual": nivel_atual,
            "temperatura_media": sum(temperaturas) / len(temperaturas),
            "altura_onda_media": sum(ondas) / len(ondas),
            "maior_onda": max(ondas),
            "vento_medio": sum(ventos) / len(ventos),
            "maior_vento": max(ventos)
        }
