from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session
from app.models import Clinic, Patient, Conversation, Message, Service, Dentist, Appointment
from app.services.gemini_agent import get_gemini_response


async def handle_incoming_message(
    channel: str, phone_number: str, message_text: str, clinic_slug: str = None
):
    async with async_session() as db:
        if clinic_slug:
            result = await db.execute(select(Clinic).where(Clinic.slug == clinic_slug))
        else:
            result = await db.execute(select(Clinic).limit(1))
        clinic = result.scalar_one_or_none()

        if not clinic:
            return

        patient_result = await db.execute(
            select(Patient).where(Patient.clinic_id == clinic.id, Patient.phone == phone_number)
        )
        patient = patient_result.scalar_one_or_none()

        if not patient:
            patient = Patient(
                clinic_id=clinic.id,
                full_name="Unknown",
                phone=phone_number,
            )
            db.add(patient)
            await db.commit()
            await db.refresh(patient)

        conv_result = await db.execute(
            select(Conversation).where(
                Conversation.clinic_id == clinic.id,
                Conversation.patient_id == patient.id,
                Conversation.channel == channel,
                Conversation.status == "active",
            )
        )
        conversation = conv_result.scalar_one_or_none()

        if not conversation:
            conversation = Conversation(
                clinic_id=clinic.id,
                patient_id=patient.id,
                channel=channel,
            )
            db.add(conversation)
            await db.commit()
            await db.refresh(conversation)

        user_msg = Message(
            conversation_id=conversation.id,
            role="user",
            content=message_text,
        )
        db.add(user_msg)
        await db.commit()

        history_result = await db.execute(
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.created_at)
        )
        messages = history_result.scalars().all()

        conversation_history = [
            {"role": m.role, "content": m.content} for m in messages[:-1]
        ]

        gemini_response = await get_gemini_response(
            clinic_name=clinic.name,
            conversation_history=conversation_history,
            user_message=message_text,
        )

        if gemini_response["type"] == "tool_call":
            tool_result = await execute_tool(
                db=db,
                tool_name=gemini_response["tool_name"],
                tool_args=gemini_response["tool_args"],
                clinic_id=clinic.id,
            )

            final_response = await get_gemini_response(
                clinic_name=clinic.name,
                conversation_history=conversation_history + [
                    {"role": "user", "content": message_text},
                    {"role": "model", "content": f"Tool result: {tool_result}"},
                ],
                user_message="Based on this tool result, provide a natural language response to the patient.",
            )

            agent_reply = final_response.get("content", "Let me help you with that.")
        else:
            agent_reply = gemini_response.get("content", "I'm here to help.")

        agent_msg = Message(
            conversation_id=conversation.id,
            role="agent",
            content=agent_reply,
        )
        db.add(agent_msg)
        conversation.last_message_at = datetime.utcnow()
        await db.commit()


async def execute_tool(
    db: AsyncSession,
    tool_name: str,
    tool_args: dict,
    clinic_id: str,
) -> str:
    if tool_name == "check_availability":
        return await check_availability(db, tool_args, clinic_id)
    elif tool_name == "book_appointment":
        return await book_appointment(db, tool_args, clinic_id)
    elif tool_name == "reschedule_appointment":
        return await reschedule_appointment(db, tool_args)
    elif tool_name == "cancel_appointment":
        return await cancel_appointment(db, tool_args)
    elif tool_name == "get_clinic_info":
        return await get_clinic_info(db, clinic_id)
    elif tool_name == "escalate_to_staff":
        return "Escalation flag set. A staff member will follow up shortly."
    return "Unknown tool"


async def check_availability(db: AsyncSession, args: dict, clinic_id: str) -> str:
    from datetime import datetime, timedelta

    start = datetime.fromisoformat(args["date_range_start"])
    end = datetime.fromisoformat(args["date_range_end"])

    result = await db.execute(
        select(Appointment).where(
            Appointment.clinic_id == clinic_id,
            Appointment.start_time >= start,
            Appointment.start_time <= end,
            Appointment.status.in_(["pending", "confirmed"]),
        )
    )
    booked = result.scalars().all()

    booked_times = {a.start_time for a in booked}

    available_slots = []
    current = start
    while current < end:
        if current not in booked_times:
            available_slots.append(current.isoformat())
        current += timedelta(minutes=30)

    if not available_slots:
        return "No available slots in the requested date range."

    return f"Available slots: {', '.join(available_slots[:10])}"


async def book_appointment(db: AsyncSession, args: dict, clinic_id: str) -> str:
    patient_result = await db.execute(
        select(Patient).where(
            Patient.clinic_id == clinic_id, Patient.phone == args["patient_phone"]
        )
    )
    patient = patient_result.scalar_one_or_none()

    if not patient:
        patient = Patient(
            clinic_id=clinic_id,
            full_name=args["patient_name"],
            phone=args["patient_phone"],
        )
        db.add(patient)
        await db.commit()
        await db.refresh(patient)

    service_result = await db.execute(select(Service).where(Service.id == args["service_id"]))
    service = service_result.scalar_one_or_none()

    if not service:
        return "Service not found."

    from datetime import timedelta

    start_time = datetime.fromisoformat(args["start_time"])
    end_time = start_time + timedelta(minutes=service.duration_minutes)

    appointment = Appointment(
        clinic_id=clinic_id,
        patient_id=patient.id,
        dentist_id=args["dentist_id"],
        service_id=args["service_id"],
        start_time=start_time,
        end_time=end_time,
        status="confirmed",
        booked_via="whatsapp",
    )
    db.add(appointment)
    await db.commit()

    return f"Appointment booked for {args['patient_name']} at {start_time.strftime('%Y-%m-%d %H:%M')} for {service.name}."


async def reschedule_appointment(db: AsyncSession, args: dict) -> str:
    from datetime import timedelta

    result = await db.execute(
        select(Appointment).where(Appointment.id == args["appointment_id"])
    )
    appointment = result.scalar_one_or_none()

    if not appointment:
        return "Appointment not found."

    service_result = await db.execute(select(Service).where(Service.id == appointment.service_id))
    service = service_result.scalar_one_or_none()

    new_start = datetime.fromisoformat(args["new_start_time"])
    new_end = new_start + timedelta(minutes=service.duration_minutes)

    appointment.start_time = new_start
    appointment.end_time = new_end
    await db.commit()

    return f"Appointment rescheduled to {new_start.strftime('%Y-%m-%d %H:%M')}."


async def cancel_appointment(db: AsyncSession, args: dict) -> str:
    result = await db.execute(
        select(Appointment).where(Appointment.id == args["appointment_id"])
    )
    appointment = result.scalar_one_or_none()

    if not appointment:
        return "Appointment not found."

    appointment.status = "cancelled"
    await db.commit()

    return "Appointment has been cancelled."


async def get_clinic_info(db: AsyncSession, clinic_id: str) -> str:
    result = await db.execute(select(Clinic).where(Clinic.id == clinic_id))
    clinic = result.scalar_one_or_none()

    services_result = await db.execute(select(Service).where(Service.clinic_id == clinic_id))
    services = services_result.scalars().all()

    services_list = "\n".join(
        [f"- {s.name}: {s.duration_minutes} min, Rs. {s.price}" for s in services]
    )

    return f"""Clinic: {clinic.name}
Address: {clinic.address}
Phone: {clinic.phone}
Timezone: {clinic.timezone}

Services:
{services_list}"""
