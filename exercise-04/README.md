# Exercise 4: focused negative and boundary tests

**25 minutes · individual · use your exercise 3 API.** You need pytest and HTTPX from the root requirements. Write `test_main.py` beside `main.py`; no running Uvicorn server is required.

## Guided first test (5 minutes)

Import `TestClient` from `fastapi.testclient` and your `app` from `main`. Create a client. In a function whose name begins `test_`, send a valid laptop JSON request with `client.post("/requests", json=body)`. Assert status 200, accepted true, and the expected quantity. Run `python -m pytest -q`.

A test sends a controlled input and asserts observable behaviour. A green result only establishes the cases and assertions you actually wrote.

## Supported negative tests (10 minutes)

Write tests for a missing student_name and a quantity below 1. Assert 422 and `response.json()["error"]["code"] == "VALIDATION_ERROR"`. Add a test for camera quantity 1; assert 409 and `EQUIPMENT_UNAVAILABLE`.

Keep a valid baseline request and change one property per case. For omitted fields, make a fresh dictionary rather than mutating a shared object that later tests depend on.

## Independent core finish (10 minutes)

Test an accepted boundary at quantity 5 and a rejected boundary at 6 using laptop. Choose one further invalid or boundary case that exposes a different risk: whitespace-only names, strict integer coercion, projector rule, or optional reason length. Explain your selection. Include at least one assertion about the body as well as the HTTP status.

Demonstrate that a relevant test detects a bug: temporarily change the corresponding rule, run that test, observe failure, restore the rule and rerun. Retain the passing output and a short description of the failure you created.

**Core evidence:** at least six behaviours: valid, missing, below-minimum, accepted maximum, application error, and independently selected case. Also check just above the maximum to complete the boundary comparison. Parametrisation is optional; separate test functions are acceptable.

**Troubleshooting:** use `python -m pytest` so the same interpreter runs; name the file `test_*.py`; inspect the actual response on failure; ensure the schema is valid when testing 409. For a deliberately demonstrated server 500, TestClient normally re-raises the server exception; `raise_server_exceptions=False` lets a test inspect the HTTP response. Do not use that setting to hide ordinary failures.

**Possible solution:** `solutions/` includes a fuller regression suite than students must write in 25 minutes. Compare coverage and reasoning, not test count. Minimum catch-up: valid, one rejected boundary, one accepted boundary and one application error; complete the remaining core cases afterwards.
