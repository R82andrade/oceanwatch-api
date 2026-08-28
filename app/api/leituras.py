from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.leitura import LeituraCreate
from app.services.leitura_service import LeituraService


router = APIRouter(
    prefix="/leituras",
    tags=["Leituras"]
)

boias_router = APIRouter(
    prefix="/boias",
    tags=["Leituras das Boias"]
)

service = LeituraService()


@router.post("/")
def criar_leitura(
    leitura: LeituraCreate,
    db: Session = Depends(get_db)
):
    return service.criar_leitura(
        db,
        leitura
    )


@router.get("/")
def listar_leituras(
    db: Session = Depends(get_db)
):
    return service.listar_leituras(db)


@boias_router.get("/{boia_id}/leituras")
def listar_leituras_por_boia(
    boia_id: int,
    db: Session = Depends(get_db)
):
    return service.listar_leituras_por_boia(
        db,
        boia_id
    )


@router.get("/{leitura_id}")
def buscar_leitura_por_id(
    leitura_id: int,
    db: Session = Depends(get_db)
):
    leitura = service.buscar_leitura_por_id(
        db,
        leitura_id
    )

    if leitura is None:
        raise HTTPException(
            status_code=404,
            detail="Leitura não encontrada."
        )

    return leitura


@router.get("/{leitura_id}/risco")
def analisar_risco(
    leitura_id: int,
    db: Session = Depends(get_db)
):
    resultado = service.analisar_risco(
        db,
        leitura_id
    )

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Leitura não encontrada."
        )

    return resultado


@router.put("/{leitura_id}")
def atualizar_leitura(
    leitura_id: int,
    dados: LeituraCreate,
    db: Session = Depends(get_db)
):
    leitura = service.atualizar_leitura(
        db,
        leitura_id,
        dados
    )

    if leitura is None:
        raise HTTPException(
            status_code=404,
            detail="Leitura não encontrada."
        )

    return leitura


@router.delete("/{leitura_id}")
def deletar_leitura(
    leitura_id: int,
    db: Session = Depends(get_db)
):
    leitura = service.deletar_leitura(
        db,
        leitura_id
    )

    if leitura is None:
        raise HTTPException(
            status_code=404,
            detail="Leitura não encontrada."
        )

    return leitura


@boias_router.get("/{boia_id}/estatisticas/temperatura")
def calcular_temperatura_media(
    boia_id: int,
    db: Session = Depends(get_db)
):
    temperatura_media = service.calcular_temperatura_media(
        db,
        boia_id
    )

    if temperatura_media is None:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma leitura encontrada para esta boia."
        )

    return {
        "boia_id": boia_id,
        "temperatura_media": round(temperatura_media, 2)
    }


@boias_router.get("/{boia_id}/resumo")
def gerar_resumo_boia(
    boia_id: int,
    db: Session = Depends(get_db)
):
    resumo = service.gerar_resumo_boia(
        db,
        boia_id
    )

    if resumo is None:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma leitura encontrada para esta boia."
        )

    return {
        "boia_id": boia_id,
        "total_leituras": resumo["total_leituras"],
        "temperatura_media": round(
            resumo["temperatura_media"], 2
        ),
        "altura_onda_media": round(
            resumo["altura_onda_media"], 2
        ),
        "maior_onda": resumo["maior_onda"],
        "vento_medio": round(
            resumo["vento_medio"], 2
        ),
        "maior_vento": resumo["maior_vento"]
    }


@boias_router.get("/{boia_id}/status")
def buscar_status_boia(
    boia_id: int,
    db: Session = Depends(get_db)
):
    leitura = service.buscar_ultima_leitura_da_boia(
        db,
        boia_id
    )

    if leitura is None:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma leitura encontrada para esta boia."
        )

    resultado = service.analisar_risco(
        db,
        leitura.id
    )

    return {
        "boia_id": boia_id,
        "leitura_id": leitura.id,
        "nivel": resultado["nivel"],
        "mensagem": resultado["mensagem"]
    }


@boias_router.get("/{boia_id}/historico-risco")
def buscar_historico_risco(
    boia_id: int,
    db: Session = Depends(get_db)
):
    historico = service.buscar_historico_risco(
        db,
        boia_id
    )

    if not historico:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma leitura encontrada para esta boia."
        )

    return {
        "boia_id": boia_id,
        "historico": historico
    }


@boias_router.get("/{boia_id}/tendencia")
def analisar_tendencia(
    boia_id: int,
    db: Session = Depends(get_db)
):
    resultado = service.analisar_tendencia(
        db,
        boia_id
    )

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Não existem leituras suficientes para analisar a tendência."
        )

    return resultado


@boias_router.get("/{boia_id}/dashboard")
def gerar_dashboard_boia(
    boia_id: int,
    db: Session = Depends(get_db)
):
    dashboard = service.gerar_dashboard_boia(
        db,
        boia_id
    )

    if dashboard is None:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma leitura encontrada para esta boia."
        )

    return {
        "boia_id": boia_id,
        "total_leituras": dashboard["total_leituras"],
        "ultima_leitura_id": dashboard["ultima_leitura_id"],
        "nivel_atual": dashboard["nivel_atual"],
        "temperatura_media": round(
            dashboard["temperatura_media"], 2
        ),
        "altura_onda_media": round(
            dashboard["altura_onda_media"], 2
        ),
        "maior_onda": dashboard["maior_onda"],
        "vento_medio": round(
            dashboard["vento_medio"], 2
        ),
        "maior_vento": dashboard["maior_vento"]
    }


@boias_router.get("/{boia_id}/painel")
def gerar_painel_boia(
    boia_id: int,
    db: Session = Depends(get_db)
):
    painel = service.gerar_painel_boia(
        db,
        boia_id
    )

    if painel is None:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma leitura encontrada para esta boia."
        )

    return {
        "boia_id": boia_id,
        **painel
    }
