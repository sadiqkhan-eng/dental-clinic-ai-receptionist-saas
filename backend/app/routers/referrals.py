from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.database import get_db
from app.models import Referral

router = APIRouter()


class ReferralCreate(BaseModel):
    clinic_id: str
    referrer_patient_id: str
    referred_patient_id: str = None


@router.get("/")
async def list_referrals(clinic_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Referral).where(Referral.clinic_id == clinic_id)
    )
    referrals = result.scalars().all()
    return [
        {
            "id": str(r.id),
            "referrer_patient_id": str(r.referrer_patient_id),
            "referred_patient_id": str(r.referred_patient_id) if r.referred_patient_id else None,
            "referral_code": r.referral_code,
            "reward_applied": r.reward_applied,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in referrals
    ]


@router.post("/")
async def create_referral(data: ReferralCreate, db: AsyncSession = Depends(get_db)):
    code = str(uuid.uuid4())[:8].upper()
    referral = Referral(
        clinic_id=data.clinic_id,
        referrer_patient_id=data.referrer_patient_id,
        referred_patient_id=data.referred_patient_id,
        referral_code=code,
    )
    db.add(referral)
    await db.commit()
    await db.refresh(referral)
    return {"id": str(referral.id), "referral_code": referral.referral_code}


@router.get("/code/{code}")
async def get_referral_by_code(code: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Referral).where(Referral.referral_code == code)
    )
    referral = result.scalar_one_or_none()
    if not referral:
        raise HTTPException(status_code=404, detail="Referral not found")
    return {
        "id": str(referral.id),
        "clinic_id": str(referral.clinic_id),
        "referral_code": referral.referral_code,
    }


@router.put("/{referral_id}/apply-reward")
async def apply_reward(referral_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Referral).where(Referral.id == referral_id))
    referral = result.scalar_one_or_none()
    if not referral:
        raise HTTPException(status_code=404, detail="Referral not found")
    referral.reward_applied = True
    await db.commit()
    return {"id": str(referral.id), "reward_applied": True}
