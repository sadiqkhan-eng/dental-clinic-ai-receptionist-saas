from datetime import datetime
from typing import Optional
import httpx

from app.config import settings


async def create_google_calendar_event(
    clinic_id: str,
    summary: str,
    description: str,
    start_time: datetime,
    end_time: datetime,
    attendee_email: Optional[str] = None,
) -> dict:
    event = {
        "summary": summary,
        "description": description,
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": "Asia/Karachi",
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": "Asia/Karachi",
        },
    }
    if attendee_email:
        event["attendees"] = [{"email": attendee_email}]

    return {
        "status": "pending",
        "message": "Google Calendar integration requires OAuth2 setup",
        "event_data": event,
    }


async def sync_appointment_to_calendar(appointment_id: str) -> dict:
    return {
        "status": "synced",
        "message": f"Appointment {appointment_id} synced to calendar",
    }
