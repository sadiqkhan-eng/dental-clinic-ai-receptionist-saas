from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import WaitingList

router = APIRouter()


class WaitingListCreate(BaseModel):
    clinic_id: str
    patient_id: str
    service_id: str = None
    preferred_date: str = None


@router.get("/")
async def list_waiting(clinic_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(WaitingList)
        .where(WaitingList.clinic_id == clinic_id, WaitingList.status == "waiting")
        .order_by(WaitingList.created_at)
    )
    items = result.scalars().all()
    return [
        {
            "id": str(w.id),
            "patient_id": str(w.patient_id),
            "service_id": str(w.service_id) if w.service_id else None,
            "preferred_date": w.preferred_date.isoformat() if w.preferred_date else None,
            "created_at": w.created_at.isoformat() if w.created_at else None,
        }
        for w in items
    ]


@router.post("/")
async def join_waiting_list(data: WaitingListCreate, db: AsyncSession = Depends(get_db)):
    item = WaitingList(
        clinic_id=data.clinic_id,
        patient_id=data.patient_id,
        service_id=data.service_id,
        preferred_date=data.preferred_date,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return {"id": str(item.id), "status": item.status}


@router.put("/{item_id}/notify")
async def notify_waiting(item_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(WaitingList).where(WaitingList.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Waiting list item not found")
    item.status = "notified"
    await db.commit()
    return {"id": str(item.id), "status": item.status}
