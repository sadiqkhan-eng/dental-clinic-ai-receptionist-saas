from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import AuditLog


async def log_action(
    db: AsyncSession,
    clinic_id: str,
    user_id: str,
    action: str,
    resource_type: str,
    resource_id: str = None,
    details: dict = None,
    ip_address: str = None,
) -> None:
    log = AuditLog(
        clinic_id=clinic_id,
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=ip_address,
    )
    db.add(log)
    await db.commit()


AUDIT_ACTIONS = {
    "clinic.update": "Updated clinic settings",
    "patient.create": "Created new patient",
    "patient.update": "Updated patient record",
    "appointment.create": "Booked new appointment",
    "appointment.cancel": "Cancelled appointment",
    "appointment.reschedule": "Rescheduled appointment",
    "service.create": "Created new service",
    "service.update": "Updated service",
    "service.delete": "Deleted service",
    "conversation.escalate": "Escalated conversation to staff",
    "staff.create": "Added new staff member",
    "staff.update": "Updated staff member",
    "invoice.create": "Created invoice",
    "invoice.pay": "Invoice paid",
}
