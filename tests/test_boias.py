from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_criar_boia():
    payload = {
        "nome": "Boia RJ-001",
        "codigo": "RJ001",
        "latitude": -22.90,
        "longitude": -43.20,
    }

    response = client.post("/boias", json=payload)

    assert response.status_code == 200
    assert response.json()["mensagem"] == "Boia cadastrada com sucesso!"
    assert response.json()["dados"]["codigo"] == "RJ001"
