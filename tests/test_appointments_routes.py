from main import app
from fastapi.testclient import TestClient
from app.core.config import settings

client = TestClient(app)


class TestAppointments:
    def setup_method(self):
        self.headers = {"Authorization": f"Bearer {settings.backend_pass}"}
        self.url = "/api/v2/appointments"

    def test_create_appointment(self):
        body = {
            "employee_name": "string",
            "time_slot": "2024-12-13T10:11",
            "description": "string",
            "position_id": 1,
            "branch_id": "ea9558c9-f877-4df2-82ba-c8130057afab"
        }
        response = client.post(url=f"{self.url}", headers=self.headers, json=body)
        assert response.status_code == 200

    def test_get_appointment_list(self):
        # Replace with a valid test token
        response = client.get(url=f"{self.url}", headers=self.headers)
        assert response.status_code == 200

