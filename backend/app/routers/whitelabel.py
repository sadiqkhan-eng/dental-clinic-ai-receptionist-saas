from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Clinic

router = APIRouter()


class DomainConfig(BaseModel):
    clinic_id: str
    custom_domain: str = None
    branding: dict = None


@router.get("/{clinic_id}/branding")
async def get_branding(clinic_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Clinic).where(Clinic.id == clinic_id))
    clinic = result.scalar_one_or_none()
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")
    return {
        "name": clinic.name,
        "branding": clinic.branding_json,
        "slug": clinic.slug,
    }


@router.put("/{clinic_id}/branding")
async def update_branding(data: DomainConfig, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Clinic).where(Clinic.id == data.clinic_id))
    clinic = result.scalar_one_or_none()
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")

    if data.branding:
        clinic.branding_json = {**clinic.branding_json, **data.branding}
    if data.custom_domain:
        clinic.branding_json["custom_domain"] = data.custom_domain

    await db.commit()
    return {"status": "updated", "branding": clinic.branding_json}


@router.get("/{clinic_id}/custom-domain")
async def get_custom_domain(clinic_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Clinic).where(Clinic.id == clinic_id))
    clinic = result.scalar_one_or_none()
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")
    custom_domain = clinic.branding_json.get("custom_domain") if clinic.branding_json else None
    return {
        "custom_domain": custom_domain,
        "default_domain": f"dentalos.app/c/{clinic.slug}",
    }
