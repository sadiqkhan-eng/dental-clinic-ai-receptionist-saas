from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Clinic

router = APIRouter()


class ClinicCreate(BaseModel):
    name: str
    slug: str


@router.get("/")
async def list_clinics(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Clinic))
    clinics = result.scalars().all()
    return [{"id": str(c.id), "name": c.name, "slug": c.slug} for c in clinics]


@router.get("/{clinic_id}")
async def get_clinic(clinic_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Clinic).where(Clinic.id == clinic_id))
    clinic = result.scalar_one_or_none()
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")
    return {
        "id": str(clinic.id),
        "name": clinic.name,
        "slug": clinic.slug,
        "phone": clinic.phone,
        "address": clinic.address,
        "timezone": clinic.timezone,
        "whatsapp_number": clinic.whatsapp_number,
        "subscription_tier": clinic.subscription_tier,
    }


@router.post("/")
async def create_clinic(data: ClinicCreate, db: AsyncSession = Depends(get_db)):
    clinic = Clinic(name=data.name, slug=data.slug)
    db.add(clinic)
    await db.commit()
    await db.refresh(clinic)
    return {"id": str(clinic.id), "name": clinic.name, "slug": clinic.slug}
