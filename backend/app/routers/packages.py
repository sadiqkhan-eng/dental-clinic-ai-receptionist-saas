from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Service

router = APIRouter()


class PackageCreate(BaseModel):
    clinic_id: str
    name: str
    service_ids: list[str]
    bundle_price: float
    description: str = None


class Package(Base):
    id: str
    name: str
    services: list
    bundle_price: float
    individual_total: float
    savings: float


@router.get("/")
async def list_packages(clinic_id: str):
    return {"packages": [], "message": "Package storage not yet implemented"}


@router.post("/")
async def create_package(data: PackageCreate, db: AsyncSession = Depends(get_db)):
    services_result = await db.execute(
        select(Service).where(Service.id.in_(data.service_ids))
    )
    services = services_result.scalars().all()

    individual_total = sum(s.price for s in services)
    savings = individual_total - data.bundle_price

    return {
        "name": data.name,
        "services": [{"id": str(s.id), "name": s.name, "price": s.price} for s in services],
        "bundle_price": data.bundle_price,
        "individual_total": individual_total,
        "savings": savings,
        "message": "Package preview - storage TBD",
    }
