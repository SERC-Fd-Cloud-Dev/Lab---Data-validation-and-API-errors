from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel, Field

class ErrorDetail(BaseModel):
    field: str
    message: str

class ErrorBody(BaseModel):
    code: str
    message: str
    details: list[ErrorDetail] = Field(default_factory=list)

class ErrorResponse(BaseModel):
    error: ErrorBody

ERROR_RESPONSES = {status: {"model": ErrorResponse} for status in (404, 409, 422)}

def install_handlers(app):
    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, exc: RequestValidationError):
        # Deliberately omit input and ctx: they can contain submitted values
        # or exception objects. Only controlled validation messages are exposed.
        details = [{"field": ".".join(map(str, e["loc"])), "message": e["msg"]}
                   for e in exc.errors()]
        return JSONResponse(status_code=422, content={"error": {
            "code": "VALIDATION_ERROR", "message": "Invalid request data",
            "details": details}})

    @app.exception_handler(StarletteHTTPException)
    async def http_error(request: Request, exc: StarletteHTTPException):
        # Routes in this teaching application supply public-safe dictionaries.
        if isinstance(exc.detail, dict):
            code = exc.detail.get("code", "HTTP_ERROR")
            message = exc.detail.get("message", "Request failed")
        else:
            code, message = "HTTP_ERROR", "Request could not be completed"
        return JSONResponse(status_code=exc.status_code, headers=exc.headers,
                            content={"error": {"code": code, "message": message,
                                               "details": []}})
