from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Dentist

router = APIRouter()


class DentistCreate(BaseModel):
    clinic_id: str
    staff_user_id: str = None
    specialty: str = None


@router.get("/")
async def list_dentists(clinic_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dentist).where(Dentist.clinic_id == clinic_id))
    dentists = result.scalars().all()
    return [
        {
            "id": str(d.id),
            "staff_user_id": str(d.staff_user_id) if d.staff_user_id else None,
            "specialty": d.specialty,
            "working_hours_json": d.working_hours_json,
        }
        for d in dentists
    ]


@router.get("/{dentist_id}")
async def get_dentist(dentist_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dentist).where(Dentist.id == dentist_id))
    dentist = result.scalar_one_or_none()
    if not dentist:
        raise HTTPException(status_code=404, detail="Dentist not found")
    return {
        "id": str(dentist.id),
        "staff_user_id": str(dentist.staff_user_id) if dentist.staff_user_id else None,
        "specialty": dentist.specialty,
        "working_hours_json": dentist.working_hours_json,
    }


@router.post("/")
async def create_dentist(data: DentistCreate, db: AsyncSession = Depends(get_db)):
    dentist = Dentist(
        clinic_id=data.clinic_id,
        staff_user_id=data.staff_user_id,
        specialty=data.specialty,
    )
    db.add(dentist)
    await db.commit()
    await db.refresh(dentist)
    return {"id": str(dentist.id), "specialty": dentist.specialty}
