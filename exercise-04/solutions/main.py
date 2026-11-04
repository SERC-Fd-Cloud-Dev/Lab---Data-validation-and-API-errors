from typing import Literal, Self
from fastapi import FastAPI, HTTPException
from errors import install_handlers, ERROR_RESPONSES
from pydantic import BaseModel, ConfigDict, Field, model_validator

app = FastAPI(title="Equipment request checker")
install_handlers(app)

# Static availability. Requests do not reserve or change stock.
STOCK = {"laptop": 5, "projector": 1, "camera": 0}

class EquipmentRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    student_name: str = Field(min_length=1, max_length=60)
    equipment_type: Literal["laptop", "projector", "camera"]
    quantity: int = Field(ge=1, le=5, strict=True)
    reason: str | None = Field(default=None, max_length=200)

    @model_validator(mode="after")
    def projector_limit(self) -> Self:
        if self.equipment_type == "projector" and self.quantity > 1:
            raise ValueError("Only one projector per request")
        return self

class RequestResult(BaseModel):
    accepted: bool
    equipment_type: str
    quantity: int

@app.post("/requests", response_model=RequestResult, responses=ERROR_RESPONSES)
def check_request(request: EquipmentRequest):
    if STOCK[request.equipment_type] < request.quantity:
        raise HTTPException(status_code=409, detail={
            "code": "EQUIPMENT_UNAVAILABLE",
            "message": "The requested equipment is unavailable"})
    return {"accepted": True, "equipment_type": request.equipment_type,
            "quantity": request.quantity, "internal_note": "not public"}
