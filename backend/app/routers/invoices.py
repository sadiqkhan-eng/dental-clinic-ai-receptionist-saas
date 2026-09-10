from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Invoice

router = APIRouter()


class InvoiceCreate(BaseModel):
    clinic_id: str
    patient_id: str
    appointment_id: str = None
    amount: float
    currency: str = "PKR"
    payment_method: str = None


@router.get("/")
async def list_invoices(clinic_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Invoice).where(Invoice.clinic_id == clinic_id)
    )
    invoices = result.scalars().all()
    return [
        {
            "id": str(inv.id),
            "patient_id": str(inv.patient_id),
            "amount": inv.amount,
            "currency": inv.currency,
            "status": inv.status,
            "payment_method": inv.payment_method,
            "created_at": inv.created_at.isoformat() if inv.created_at else None,
        }
        for inv in invoices
    ]


@router.post("/")
async def create_invoice(data: InvoiceCreate, db: AsyncSession = Depends(get_db)):
    invoice = Invoice(
        clinic_id=data.clinic_id,
        patient_id=data.patient_id,
        appointment_id=data.appointment_id,
        amount=data.amount,
        currency=data.currency,
        payment_method=data.payment_method,
    )
    db.add(invoice)
    await db.commit()
    await db.refresh(invoice)
    return {"id": str(invoice.id), "status": invoice.status}


@router.put("/{invoice_id}/pay")
async def mark_paid(
    invoice_id: str,
    payment_method: str,
    payment_reference: str = None,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Invoice).where(Invoice.id == invoice_id))
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    invoice.status = "paid"
    invoice.payment_method = payment_method
    invoice.payment_reference = payment_reference
    await db.commit()
    return {"id": str(invoice.id), "status": invoice.status}
