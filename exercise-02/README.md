# Exercise 2: strengthen the input contract

**25 minutes · individual · continue your own exercise 1 application.** No starter code, database or CRUD. Save a working checkpoint before changing your model.

## 1. Guided pattern (5 minutes)

`Field(ge=1, le=5)` expresses an inclusive numeric range. Import `Field` and apply it to quantity. Predict outcomes for 0, 1, 5 and 6, then send requests. Expected: 422, 200, 200 and 422 for laptop requests.

Add `strict=True` to that field. Repeat with JSON number `2`, string `"2"` and boolean `true`. Only the number passes. This strictness decision applies to quantity, not automatically to every field.

## 2. Supported practice (10 minutes)

Implement these requirements in `EquipmentRequest`:

| Field/policy | Required behaviour |
|---|---|
| student_name | Strip surrounding whitespace; length 1–60 after stripping |
| equipment_type | Exactly laptop, projector or camera (lowercase) |
| quantity | Strict integer, inclusive range 1–5 |
| reason | May be omitted or null; otherwise maximum 200 characters after stripping; empty string permitted |
| Unknown fields | Reject rather than silently ignore |

Use `ConfigDict(str_strip_whitespace=True, extra="forbid")` as the model configuration, `Literal` for the finite category list, and `str | None` with `default=None` for reason. Why does `str | None` alone still require a supplied value? It permits null; the default permits omission.

Check a blank name, a 60-character name, a 61-character name, omitted reason, null reason and a 201-character reason. Expected: 422, 200, 422, 200, 200, 422. Keep quantity/type valid while testing names. Changing several fields at once hides which rule you have verified.

## 3. Independent core finish (10 minutes)

New requirement: each request may contain at most one projector. Implement a model-level after-validator that checks the relationship between equipment_type and quantity. Choose a clear message. Do not write a database lookup.

An after-validator receives the already validated instance. Use `@model_validator(mode="after")`, raise `ValueError` for a failed request rule, and return the instance when it passes. You decide the conditional expression and method name.

Acceptance checks: projector quantity 1 gives 200; projector quantity 2 gives 422; laptop quantity 2 still gives 200. Explain why quantity 2 is valid in one request and invalid in another.

**Hints, in order:** compare two model attributes; put the condition inside the method; return `self` outside the failing branch. If validation crashes, inspect indentation and make sure ValueError is raised, not returned.

**Evidence:** updated model, boundary observations, and one justified additional case of your own. Explain which constraints appear in OpenAPI and why a custom cross-field rule may need written documentation as well.

**Possible solution:** `solutions/`. Minimum catch-up is the quantity range and blank-name rule; complete the cross-field rule before exercise 3. Optional extension: compare an enum with Literal and justify when you would choose each.
