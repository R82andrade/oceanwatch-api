def test_painel_boia(client):
    response = client.get("/boias/7/painel")

    assert response.status_code == 200

    data = response.json()

    assert data["boia_id"] == 7

    assert "dashboard" in data
    assert "tendencia" in data
    assert "historico_risco" in data

    dashboard = data["dashboard"]

    assert dashboard["total_leituras"] == 5
    assert dashboard["ultima_leitura_id"] == 5
    assert dashboard["nivel_atual"] == "RISCO"

    assert dashboard["temperatura_media"] == 25.36
    assert dashboard["altura_onda_media"] == 3.1
    assert dashboard["maior_onda"] == 5
    assert dashboard["vento_medio"] == 23.74
    assert dashboard["maior_vento"] == 30

    tendencia = data["tendencia"]

    assert tendencia["nivel_atual"] == "RISCO"
    assert tendencia["nivel_anterior"] == "RISCO"
    assert tendencia["tendencia"] == "ESTAVEL"

    historico = data["historico_risco"]

    assert len(historico) == 5


def test_painel_boia_sem_leituras(client):
    response = client.get("/boias/999/painel")

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Nenhuma leitura encontrada para esta boia."
