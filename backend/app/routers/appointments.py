from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Appointment, Service

router = APIRouter()


class AppointmentCreate(BaseModel):
    clinic_id: str
    patient_id: str
    dentist_id: str
    service_id: str
    start_time: str
    booked_via: str = "staff"
    notes: str = None


@router.get("/")
async def list_appointments(clinic_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Appointment).where(Appointment.clinic_id == clinic_id)
    )
    appointments = result.scalars().all()
    return [
        {
            "id": str(a.id),
            "patient_id": str(a.patient_id),
            "dentist_id": str(a.dentist_id),
            "service_id": str(a.service_id),
            "start_time": a.start_time.isoformat(),
            "end_time": a.end_time.isoformat(),
            "status": a.status,
            "booked_via": a.booked_via,
            "notes": a.notes,
        }
        for a in appointments
    ]


@router.get("/{appointment_id}")
async def get_appointment(appointment_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Appointment).where(Appointment.id == appointment_id)
    )
    appointment = result.scalar_one_or_none()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {
        "id": str(appointment.id),
        "patient_id": str(appointment.patient_id),
        "dentist_id": str(appointment.dentist_id),
        "service_id": str(appointment.service_id),
        "start_time": appointment.start_time.isoformat(),
        "end_time": appointment.end_time.isoformat(),
        "status": appointment.status,
        "booked_via": appointment.booked_via,
        "notes": appointment.notes,
    }


@router.post("/")
async def create_appointment(data: AppointmentCreate, db: AsyncSession = Depends(get_db)):
    service_result = await db.execute(select(Service).where(Service.id == data.service_id))
    service = service_result.scalar_one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    start = datetime.fromisoformat(data.start_time)
    end = start + timedelta(minutes=service.duration_minutes)

    appointment = Appointment(
        clinic_id=data.clinic_id,
        patient_id=data.patient_id,
        dentist_id=data.dentist_id,
        service_id=data.service_id,
        start_time=start,
        end_time=end,
        booked_via=data.booked_via,
        notes=data.notes,
    )
    db.add(appointment)
    await db.commit()
    await db.refresh(appointment)
    return {"id": str(appointment.id), "status": appointment.status}


@router.put("/{appointment_id}/status")
async def update_appointment_status(
    appointment_id: str, status: str, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Appointment).where(Appointment.id == appointment_id)
    )
    appointment = result.scalar_one_or_none()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointment.status = status
    await db.commit()
    return {"id": str(appointment.id), "status": appointment.status}
