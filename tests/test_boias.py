import uuid

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_criar_boia():
    numero_serie = f"TEST-{uuid.uuid4()}"
    payload = {
        "nome": "Boia Teste",
        "numero_serie": numero_serie,
        "latitude": -22.90,
        "longitude": -43.20,
    }

    response = client.post("/boias", json=payload)

    assert response.status_code == 200
    assert response.json()["nome"] == "Boia Teste"
    assert response.json()["numero_serie"] == numero_serie
