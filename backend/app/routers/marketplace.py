from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Clinic

router = APIRouter()


@router.get("/clinics")
async def search_clinics(
    city: str = None,
    specialty: str = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Clinic)
    result = await db.execute(query)
    clinics = result.scalars().all()

    return [
        {
            "id": str(c.id),
            "name": c.name,
            "address": c.address,
            "phone": c.phone,
            "slug": c.slug,
        }
        for c in clinics
    ]


@router.get("/clinics/{slug}")
async def get_clinic_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Clinic).where(Clinic.slug == slug))
    clinic = result.scalar_one_or_none()
    if not clinic:
        return {"error": "Clinic not found"}, 404

    from app.models import Service, Dentist
    services = await db.execute(select(Service).where(Service.clinic_id == clinic.id))
    dentists = await db.execute(select(Dentist).where(Dentist.clinic_id == clinic.id))

    return {
        "id": str(clinic.id),
        "name": clinic.name,
        "address": clinic.address,
        "phone": clinic.phone,
        "services": [{"name": s.name, "price": s.price} for s in services.scalars().all()],
        "dentists": [{"specialty": d.specialty} for d in dentists.scalars().all()],
    }
