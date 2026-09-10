from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db
from app.models import Clinic

router = APIRouter()


async def verify_api_key(x_api_key: Optional[str] = Header(None), db: AsyncSession = Depends(get_db)):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required")
    return x_api_key


@router.get("/v1/clinics")
async def api_list_clinics(api_key: str = Depends(verify_api_key), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Clinic))
    clinics = result.scalars().all()
    return [
        {"id": str(c.id), "name": c.name, "slug": c.slug}
        for c in clinics
    ]


@router.get("/v1/clinics/{clinic_id}")
async def api_get_clinic(clinic_id: str, api_key: str = Depends(verify_api_key), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Clinic).where(Clinic.id == clinic_id))
    clinic = result.scalar_one_or_none()
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")
    return {"id": str(clinic.id), "name": clinic.name, "slug": clinic.slug}


@router.get("/v1/clinics/{clinic_id}/appointments")
async def api_get_appointments(clinic_id: str, api_key: str = Depends(verify_api_key), db: AsyncSession = Depends(get_db)):
    from app.models import Appointment
    result = await db.execute(
        select(Appointment).where(Appointment.clinic_id == clinic_id)
    )
    appointments = result.scalars().all()
    return [
        {
            "id": str(a.id),
            "start_time": a.start_time.isoformat(),
            "status": a.status,
        }
        for a in appointments
    ]


@router.get("/docs")
async def api_docs():
    return {
        "title": "DentalOS API",
        "version": "v1",
        "endpoints": {
            "GET /api/access/v1/clinics": "List all clinics",
            "GET /api/access/v1/clinics/{id}": "Get clinic details",
            "GET /api/access/v1/clinics/{id}/appointments": "Get clinic appointments",
        },
        "authentication": "Pass X-Api-Key header",
    }
