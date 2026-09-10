from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import StaffUser

router = APIRouter()


class StaffCreate(BaseModel):
    clerk_user_id: str
    clinic_id: str
    role: str = "receptionist"
    full_name: str = None
    phone: str = None


@router.get("/")
async def list_staff(clinic_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(StaffUser).where(StaffUser.clinic_id == clinic_id)
    )
    staff = result.scalars().all()
    return [
        {
            "id": str(s.id),
            "clerk_user_id": s.clerk_user_id,
            "role": s.role,
            "full_name": s.full_name,
            "phone": s.phone,
        }
        for s in staff
    ]


@router.get("/by-clerk/{clerk_user_id}")
async def get_staff_by_clerk_id(clerk_user_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(StaffUser).where(StaffUser.clerk_user_id == clerk_user_id)
    )
    staff = result.scalar_one_or_none()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff user not found")
    return {
        "id": str(staff.id),
        "clerk_user_id": staff.clerk_user_id,
        "clinic_id": str(staff.clinic_id),
        "role": staff.role,
        "full_name": staff.full_name,
        "phone": staff.phone,
    }


@router.post("/")
async def create_staff(data: StaffCreate, db: AsyncSession = Depends(get_db)):
    staff = StaffUser(
        clerk_user_id=data.clerk_user_id,
        clinic_id=data.clinic_id,
        role=data.role,
        full_name=data.full_name,
        phone=data.phone,
    )
    db.add(staff)
    await db.commit()
    await db.refresh(staff)
    return {"id": str(staff.id), "role": staff.role}
