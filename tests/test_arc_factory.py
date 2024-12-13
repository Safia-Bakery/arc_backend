from main import app

from fastapi.testclient import TestClient

from app.core.config import settings
client = TestClient(app)


def test_arc_requests():
    # Replace with a valid test token
    headers = {"Authorization": f"Bearer {settings.backend_pass}"}

    response = client.get("/api/v2/arc/factory/divisions", headers=headers, )
    assert response.status_code == 200

