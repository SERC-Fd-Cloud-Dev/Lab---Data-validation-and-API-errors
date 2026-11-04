# Exercise 3: make failures predictable

**35 minutes · individual · extend your own validated API.** Retain exercise 2 rules. The lecturer's parcel example demonstrates the mechanism; your implementation applies it to equipment.

## 1. Guided application error (8 minutes)

Create a static catalogue in your file: laptop has 5 available, projector 1 and camera 0. A request does not change these numbers. In the route, compare requested quantity with availability after Pydantic validation succeeds. Import and raise `HTTPException` with status 409 when stock cannot meet the request. Supply public-safe detail containing code `EQUIPMENT_UNAVAILABLE` and message `The requested equipment is unavailable`.

Checkpoint: camera quantity 1 gives 409; laptop quantity 1 gives 200; laptop quantity 0 still gives 422. FastAPI's default HTTPException response wraps your dictionary under `detail`. Raising the exception stops normal route execution.

## 2. Supported consistent responses (17 minutes)

A client should not need a different outer error structure for each failure. Use this contract:

```json
{"error":{"code":"EQUIPMENT_UNAVAILABLE","message":"The requested equipment is unavailable","details":[]}}
```

Create `errors.py` and write an `install_handlers(app)` function. The demonstrated pattern is available in the tutor demonstration during class; these steps also explain what to build independently:

1. Register an async handler for `RequestValidationError` using `app.exception_handler`. It accepts `request` and `exc`, and returns `JSONResponse` with status 422.
2. Read `exc.errors()`. For each error, copy only `loc` (joined with dots into `field`) and `msg` (as `message`) to a details list. Do not copy `input`, `ctx`, raw request bodies or exception strings.
3. Set code to `VALIDATION_ERROR`, message to `Invalid request data`, and details to that list.
4. Register a handler for Starlette's `HTTPException`, which also catches FastAPI HTTPException and router errors. Return the same envelope, use `exc.status_code`, and preserve `exc.headers`.
5. For the public-safe dictionary you supplied, take code/message from detail. For other HTTP errors, use `HTTP_ERROR` and `Request could not be completed`, with an empty details list.
6. Import and call your installer once after creating `app` in main.py.

JSONResponse takes `status_code=...` and `content=...`. A request validation handler changes presentation of failed input, not the Pydantic rules themselves. For this exercise the validator messages are controlled, public-safe strings. A broader system may need a stricter error-message allowlist.

Checkpoint: quantity 0 returns 422 with error.code VALIDATION_ERROR and a detail field of body.quantity. Camera quantity 1 returns the exact 409 body above. An unknown URL returns 404 in the same outer structure. Avoid asserting exact framework-generated message wording.

## 3. Independent core finish (10 minutes)

Document the custom error contract in OpenAPI. Define small Pydantic models for an error detail, error body and outer response. Give the details list a default factory. Use a `responses` mapping in the route decorator for 409 and 422 (and 404 where relevant). Inspect `/openapi.json` and Swagger UI to verify they name your error schema.

Choose a new failing request and explain both its status and its error fields. Write one sentence on why returning a 200 body with `accepted:false` would be an unsuitable replacement for this unavailable-stock error policy.

**Hints:** exception handlers return responses, they do not raise the same exception again; use the Starlette exception class in registration; adding a response model to OpenAPI documents the handler's output but does not automatically validate JSONResponse bodies.

**Evidence:** one 422 and one 409 response, one router 404, documented schema, and your explanation. No custom exception hierarchy is required. `solutions/` is a possible implementation for later comparison.
