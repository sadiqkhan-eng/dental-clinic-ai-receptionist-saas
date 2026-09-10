from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Service

router = APIRouter()


@router.get("/")
async def list_services(clinic_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Service).where(Service.clinic_id == clinic_id))
    services = result.scalars().all()
    return [
        {
            "id": str(s.id),
            "name": s.name,
            "duration_minutes": s.duration_minutes,
            "price": s.price,
            "category": s.category,
        }
        for s in services
    ]


@router.post("/")
async def create_service(
    clinic_id: str,
    name: str,
    duration_minutes: int,
    price: float,
    category: str = None,
    db: AsyncSession = Depends(get_db),
):
    service = Service(
        clinic_id=clinic_id,
        name=name,
        duration_minutes=duration_minutes,
        price=price,
        category=category,
    )
    db.add(service)
    await db.commit()
    await db.refresh(service)
    return {"id": str(service.id), "name": service.name}
