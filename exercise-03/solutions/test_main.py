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

import pytest

@pytest.mark.parametrize("quantity,status", [(0,422),(1,200),(5,200),(6,422), ("2",422),(True,422)])
def test_quantity_boundaries_and_types(quantity, status):
    assert client.post("/requests", json={**VALID,"quantity":quantity}).status_code == status

@pytest.mark.parametrize("name,status", [(" ",422),("A",200),("A"*60,200),("A"*61,422)])
def test_name(name,status):
    assert client.post("/requests",json={**VALID,"student_name":name}).status_code == status

@pytest.mark.parametrize("reason,status", [(None,200),("",200),("x"*200,200),("x"*201,422)])
def test_reason(reason,status):
    assert client.post("/requests",json={**VALID,"reason":reason}).status_code == status

def test_omitted_reason():
    body=VALID.copy(); del body["reason"]
    assert client.post("/requests",json=body).status_code == 200

def test_projector_rule():
    r=client.post("/requests",json={**VALID,"equipment_type":"projector","quantity":2})
    assert r.status_code == 422
    assert client.post("/requests",json={**VALID,"equipment_type":"projector","quantity":1}).status_code == 200

def test_unknown_category_and_extra_field():
    assert client.post("/requests",json={**VALID,"equipment_type":"drone"}).status_code == 422
    assert client.post("/requests",json={**VALID,"debug":True}).status_code == 422

def test_unavailable():
    r=client.post("/requests",json={**VALID,"equipment_type":"camera","quantity":1})
    assert r.status_code == 409
    assert r.json() == {"error":{"code":"EQUIPMENT_UNAVAILABLE", "message":"The requested equipment is unavailable", "details":[]}}

def test_validation_envelope():
    r=client.post("/requests",json={**VALID,"quantity":0})
    assert r.status_code == 422
    e=r.json()["error"]
    assert e["code"] == "VALIDATION_ERROR"
    assert e["details"][0]["field"] == "body.quantity"
    assert "input" not in str(e) and "ctx" not in str(e)

def test_framework_404():
    r=client.get("/not-a-route")
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "HTTP_ERROR"

def test_malformed_json():
    r=client.post("/requests",content='{"quantity":',headers={"Content-Type":"application/json"})
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "VALIDATION_ERROR"

def test_openapi_contract():
    schema=client.get("/openapi.json").json()
    responses=schema["paths"]["/requests"]["post"]["responses"]
    assert responses["422"]["content"]["application/json"]["schema"]["$ref"].endswith("ErrorResponse")
