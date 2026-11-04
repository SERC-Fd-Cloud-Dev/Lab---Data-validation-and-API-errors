from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
VALID = {"student_name": "Alex", "equipment_type": "laptop", "quantity": 2,
         "reason": "Class demonstration"}

def test_valid_and_response_filter():
    r = client.post("/requests", json=VALID)
    assert r.status_code == 200
    assert r.json() == {"accepted": True, "equipment_type": "laptop", "quantity": 2}

def test_missing_name():
    body = VALID.copy()
    del body["student_name"]
    assert client.post("/requests", json=body).status_code == 422
