from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Patient

router = APIRouter()


class PatientCreate(BaseModel):
    clinic_id: str
    full_name: str
    phone: str


@router.get("/")
async def list_patients(clinic_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Patient).where(Patient.clinic_id == clinic_id))
    patients = result.scalars().all()
    return [
        {
            "id": str(p.id),
            "full_name": p.full_name,
            "phone": p.phone,
            "email": p.email,
            "dob": str(p.dob) if p.dob else None,
        }
        for p in patients
    ]


@router.get("/{patient_id}")
async def get_patient(patient_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Patient).where(Patient.id == patient_id))
    patient = result.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {
        "id": str(patient.id),
        "full_name": patient.full_name,
        "phone": patient.phone,
        "email": patient.email,
        "dob": str(patient.dob) if patient.dob else None,
    }


@router.post("/")
async def create_patient(data: PatientCreate, db: AsyncSession = Depends(get_db)):
    patient = Patient(clinic_id=data.clinic_id, full_name=data.full_name, phone=data.phone)
    db.add(patient)
    await db.commit()
    await db.refresh(patient)
    return {"id": str(patient.id), "full_name": patient.full_name}
