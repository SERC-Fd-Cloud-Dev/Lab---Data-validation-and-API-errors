from fastapi.testclient import TestClient
from main import app
import pytest
client=TestClient(app)
VALID={"movie_title":"Jaws","attempt_number":1}

def test_correct():
    r=client.post("/rounds/1/guess",json=VALID)
    assert r.status_code==200
    assert r.json()=={"round_id":1,"correct":True}

def test_incorrect_is_normal_result():
    r=client.post("/rounds/1/guess",json={**VALID,"movie_title":"Alien"})
    assert r.status_code==200 and r.json()["correct"] is False

def test_normalisation():
    assert client.post("/rounds/1/guess",json={**VALID,"movie_title":"  jAwS  "}).json()["correct"] is True

@pytest.mark.parametrize("n,status",[(0,422),(1,200),(5,200),(6,422),("1",422),(True,422)])
def test_attempt_boundaries(n,status):
    assert client.post("/rounds/1/guess",json={**VALID,"attempt_number":n}).status_code==status

@pytest.mark.parametrize("title,status",[("",422),("   ",422),("x"*100,200),("x"*101,422)])
def test_title(title,status):
    assert client.post("/rounds/1/guess",json={**VALID,"movie_title":title}).status_code==status

def test_missing_title():
    r=client.post("/rounds/1/guess",json={"attempt_number":1})
    assert r.status_code==422 and r.json()["error"]["code"]=="VALIDATION_ERROR"

@pytest.mark.parametrize("round_id,status",[(99,404),(0,422),("abc",422)])
def test_round_id(round_id,status):
    r=client.post(f"/rounds/{round_id}/guess",json=VALID)
    assert r.status_code==status
    if status==404:
        assert r.json()=={"error":{"code":"ROUND_NOT_FOUND","message":"Round not found","details":[]}}

def test_no_answer_leak():
    r=client.post("/rounds/2/guess",json=VALID)
    assert set(r.json())=={"round_id","correct"}
