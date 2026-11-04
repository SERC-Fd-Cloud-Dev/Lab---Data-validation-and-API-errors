---
name: testing
description: "Generate permitted unit and integration tests with pytest, FastAPI, fixtures, mocks and authorisation checks."
---


# Automated Testing — Generation Permitted

Complete test code is explicitly allowed by the
current assessment brief.

## Process

1. Inspect the student's actual interfaces,
   expectations and existing test conventions.
2. Identify the test level: unit or integration.
3. Identify expected outputs and error conditions.
4. Generate meaningful tests using the actual API.
5. Explain what every test verifies.
6. Ask the student to run and review the tests.

Permitted:

- pytest tests
- FastAPI TestClient integration tests
- Test fixtures and mocks
- Parametrised cases
- Boundary and invalid-input tests
- Authentication and authorisation tests
- Mocked upstream API failure cases
- Test-only database setup

Only edit test files and test-specific helpers.

Never generate or modify production implementation.
Never change dependencies, workflows or configuration.
Never weaken an assertion merely to pass a test.
Never claim tests passed unless observed.

When code is defective, explain the diagnosis;
the student must fix the application.

Remind students to declare generated tests.
