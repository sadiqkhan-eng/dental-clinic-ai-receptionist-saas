from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class InsuranceCheck(BaseModel):
    patient_id: str
    insurance_provider: str
    policy_number: str


@router.post("/verify")
async def verify_insurance(data: InsuranceCheck):
    return {
        "verified": True,
        "provider": data.insurance_provider,
        "policy_number": data.policy_number,
        "coverage": "Basic dental coverage",
        "message": "Insurance verification requires provider API integration",
    }


@router.get("/providers")
async def list_providers():
    return [
        {"id": "1", "name": "State Life Insurance"},
        {"id": "2", "name": "EFU Life Assurance"},
        {"id": "3", "name": "Jubilee Insurance"},
        {"id": "4", "name": "Adamjee Insurance"},
    ]
