# Homework: movie guessing game

**60 minutes · independent formative practice.** Build a new small FastAPI application. Reuse your understanding and your generic error-handler pattern; do not copy the equipment application and only rename it. There is no database, CRUD, score tracking, authentication or external API.

## Scenario and fixed data

A player submits a title for a known clue. Use these two fixed rounds in a Python dictionary:

| Round | Clue | Answer, held by server |
|---|---|---|
| 1 | A shark threatens a seaside town | Jaws |
| 2 | Toys have a secret life | Toy Story |

The clue table is sufficient for testing. A clue-fetching endpoint is not required.

## API contract

Create `POST /rounds/{round_id}/guess` with request and response Pydantic models.

```json
{"movie_title":"Jaws","attempt_number":2}
```

| Requirement | Expected behaviour |
|---|---|
| movie_title | Required string, strip surrounding whitespace, length 1–100 |
| attempt_number | Required strict integer, 1–5 inclusive |
| Unexpected body field | Reject with 422 |
| round_id | Positive integer path parameter; invalid type or non-positive value gives 422 |
| Existing round, correct guess | 200 with round_id and correct true |
| Existing round, incorrect guess | 200 with round_id and correct false |
| Unknown positive round | 404 with code ROUND_NOT_FOUND, message Round not found, details [] |
| Invalid request | 422 with the shared error/code/message/details envelope |

Compare titles case-insensitively after stripping whitespace. Do not return the stored answer or internal data. Document the error response models in OpenAPI. Unknown round checks should use an otherwise valid body when testing 404.

**Important distinction:** an incorrect but valid guess is a normal game outcome. Attempt number is only a validated client-supplied value: this stateless API does not enforce a real attempt limit or remember previous guesses.

## Work plan

- 0–10 minutes: create an empty project and reuse the tested environment setup.
- 10–25: define models and input constraints.
- 25–40: implement comparison and unknown-round response; adapt the generic error-handler pattern.
- 40–55: test a correct guess, incorrect guess, blank title, missing title, attempts 1/5/0/6 and an unknown round. Parametrise if familiar.
- 55–60: record results and explain one design choice.

## Independent choices and evidence

Choose clear class/function names and one additional case (for example mixed case or a 101-character title). Retain your code, passing tests, the extra case's purpose and a two-sentence explanation of why an incorrect guess uses 200.

**Self-check:** round 1 with `"  jAwS  "` is correct; round 1 with `"Alien"` is incorrect with 200; round 99 with a valid body gives 404; title `"   "` gives 422. Responses never contain the answer.

**Hints:** use `Path(ge=1)` for the path constraint; check dictionary membership before indexing; `casefold()` supports case-insensitive string comparisons. If you see 422 instead of 404, first make the body valid. Do not implement tracking or randomisation to solve this homework.

**Possible solution:** `solutions/`, to consult after your own attempt. Optional extension after finishing: add a test proving the answer never appears in any successful response. Bring your results and one question to the review class.
