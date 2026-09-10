from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from app.database import get_db
from app.models import Appointment, Patient, Invoice

router = APIRouter()


@router.get("/summary")
async def get_summary(clinic_id: str, db: AsyncSession = Depends(get_db)):
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    appointments_today = await db.execute(
        select(func.count(Appointment.id)).where(
            Appointment.clinic_id == clinic_id,
            Appointment.start_time >= today,
            Appointment.start_time < today + timedelta(days=1),
        )
    )
    total_patients = await db.execute(
        select(func.count(Patient.id)).where(Patient.clinic_id == clinic_id)
    )
    total_revenue = await db.execute(
        select(func.coalesce(func.sum(Invoice.amount), 0)).where(
            Invoice.clinic_id == clinic_id, Invoice.status == "paid"
        )
    )

    return {
        "appointments_today": appointments_today.scalar() or 0,
        "total_patients": total_patients.scalar() or 0,
        "total_revenue": float(total_revenue.scalar() or 0),
    }


@router.get("/revenue")
async def get_revenue_chart(clinic_id: str, months: int = 6, db: AsyncSession = Depends(get_db)):
    results = []
    now = datetime.utcnow()
    for i in range(months - 1, -1, -1):
        month_start = (now.replace(day=1) - timedelta(days=30 * i)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if month_start.month == 12:
            month_end = month_start.replace(year=month_start.year + 1, month=1)
        else:
            month_end = month_start.replace(month=month_start.month + 1)

        revenue = await db.execute(
            select(func.coalesce(func.sum(Invoice.amount), 0)).where(
                Invoice.clinic_id == clinic_id,
                Invoice.status == "paid",
                Invoice.created_at >= month_start,
                Invoice.created_at < month_end,
            )
        )
        results.append({
            "month": month_start.strftime("%Y-%m"),
            "revenue": float(revenue.scalar() or 0),
        })
    return results


@router.get("/appointments-by-service")
async def get_appointments_by_service(clinic_id: str, db: AsyncSession = Depends(get_db)):
    from app.models import Service

    result = await db.execute(
        select(Service.name, func.count(Appointment.id))
        .join(Appointment, Appointment.service_id == Service.id)
        .where(Service.clinic_id == clinic_id)
        .group_by(Service.name)
    )
    return [{"service": row[0], "count": row[1]} for row in result.all()]


@router.get("/no-show-rate")
async def get_no_show_rate(clinic_id: str, db: AsyncSession = Depends(get_db)):
    total = await db.execute(
        select(func.count(Appointment.id)).where(Appointment.clinic_id == clinic_id)
    )
    no_shows = await db.execute(
        select(func.count(Appointment.id)).where(
            Appointment.clinic_id == clinic_id,
            Appointment.status == "no_show",
        )
    )
    total_count = total.scalar() or 0
    no_show_count = no_shows.scalar() or 0
    rate = (no_show_count / total_count * 100) if total_count > 0 else 0
    return {"total_appointments": total_count, "no_shows": no_show_count, "rate": round(rate, 2)}
