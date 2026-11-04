from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Equipment request checker")

class EquipmentRequest(BaseModel):
    student_name: str
    equipment_type: str
    quantity: int
    reason: str

class RequestResult(BaseModel):
    accepted: bool
    equipment_type: str
    quantity: int

@app.post("/requests", response_model=RequestResult)
def check_request(request: EquipmentRequest):
    return {"accepted": True, "equipment_type": request.equipment_type,
            "quantity": request.quantity, "internal_note": "not public"}
