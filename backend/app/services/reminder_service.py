from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session
from app.models import Appointment, Patient, Clinic
from app.config import settings


async def send_sms(to: str, body: str) -> bool:
    try:
        from twilio.rest import Client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(body=body, from_=settings.TWILIO_PHONE_NUMBER, to=to)
        return True
    except Exception:
        return False


async def send_email(to: str, subject: str, body: str) -> bool:
    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
        message = Mail(
            from_email=settings.SENDGRID_FROM_EMAIL,
            to_emails=to,
            subject=subject,
            html_content=body,
        )
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        sg.send(message)
        return True
    except Exception:
        return False


async def send_appointment_reminders():
    async with async_session() as db:
        tomorrow = datetime.utcnow() + timedelta(days=1)
        start = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)

        result = await db.execute(
            select(Appointment, Patient, Clinic)
            .join(Patient, Appointment.patient_id == Patient.id)
            .join(Clinic, Appointment.clinic_id == Clinic.id)
            .where(
                Appointment.start_time >= start,
                Appointment.start_time < end,
                Appointment.status == "confirmed",
            )
        )
        appointments = result.all()

        for apt, patient, clinic in appointments:
            time_str = apt.start_time.strftime("%I:%M %p")
            msg = f"Reminder: You have an appointment at {clinic.name} tomorrow at {time_str}. Reply CONFIRM to confirm or CANCEL to cancel."

            if patient.phone:
                await send_sms(patient.phone, msg)
            if patient.email:
                await send_email(patient.email, f"Appointment Reminder - {clinic.name}", msg)
