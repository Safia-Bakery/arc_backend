from main import app

from fastapi.testclient import TestClient

from app.core.config import settings
client = TestClient(app)

# def test_read_root():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"message": "Hello, World!"}


def test_excell_file():
    # Replace with a valid test token
    headers = {"Authorization": f"Bearer {settings.backend_pass}"}
    payload = {
        "finish_date": "2024-12-13",
        "start_date":"2024-12-11"
    }
    response = client.post("/it/excell", headers=headers,json=payload)
    assert response.status_code == 200


def test_it_requests():
    # Replace with a valid test token
    headers = {"Authorization": f"Bearer {settings.backend_pass}"}

    response = client.get("/api/v2/requests/it", headers=headers, )
    assert response.status_code == 200







