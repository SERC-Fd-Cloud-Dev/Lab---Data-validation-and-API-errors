# Exercise 1: build a request-checking API

**30 minutes · individual · start with an empty project.** Build request and response models and explain what FastAPI checks automatically. Follow the environment steps in the root README first. You create every application file yourself.

## 1. Guided start: create the application (8 minutes)

Create `main.py`. Import `FastAPI` from `fastapi` and `BaseModel` from `pydantic`. Instantiate an application named `app`. A class that inherits `BaseModel` describes a data contract. Its annotated attributes become fields.

Write an `EquipmentRequest` model with four required fields: `student_name: str`, `equipment_type: str`, `quantity: int` and `reason: str`. At this stage, add no limits or business rules. Run the server using the root instructions. Seeing `/docs` confirms the app imports; it does not yet prove a route works.

## 2. Guided application: connect a route (8 minutes)

Define `RequestResult` with `accepted: bool`, `equipment_type: str` and `quantity: int`. Decorate a function with a POST route at `/requests`; specify `response_model=RequestResult`. Give the function one parameter annotated with `EquipmentRequest`. FastAPI treats this model parameter as the JSON body.

Return a dictionary with accepted set to true and the equipment type/quantity from the model instance. This operation only checks a request. Use the default `200` because no resource is saved. Add an extra `internal_note` key to the returned dictionary and inspect whether it appears in the response.

Checkpoint: submit this JSON through Swagger UI:

```json
{"student_name":"Alex","equipment_type":"laptop","quantity":2,"reason":"Class demonstration"}
```

Expected: `200`, with exactly `{"accepted":true,"equipment_type":"laptop","quantity":2}`. The response model filters the extra internal field. Do not return private data in the first place in a real service; filtering is an additional boundary.

## 3. Supported investigation (7 minutes)

Predict, send and record the outcome of each change separately: omit student_name; set quantity to `"2"`; set quantity to `"two"`; set quantity to `0`. Keep all other fields valid.

Expected: missing name is `422`; `"2"` is parsed to an integer and accepted; `"two"` is rejected; `0` is accepted because you have not declared a lower limit. A Python annotation alone does not mean strict validation.

## 4. Independent core finish (7 minutes)

Choose one other required field to omit and one returned value to inspect. Explain how you can tell input validation from response filtering. Temporarily return a value that cannot satisfy the response model, observe the server-side error, then undo the deliberate defect. Do not turn this bug into a client `422`.

**Finish:** retain your working file, a four-row prediction/result record, and a sentence explaining why `0` passed. Show that your API stores nothing.

**Hints:** check the decorator's `response_model`; access model fields as attributes; distinguish the function parameter from its model class. If `/docs` is empty, confirm that the decorated function is in the imported module.

**Possible solution:** `solutions/` contains one implementation and tests. Compare after attempting the exercise. For catch-up, first obtain the exact successful response and one missing-field `422`.
