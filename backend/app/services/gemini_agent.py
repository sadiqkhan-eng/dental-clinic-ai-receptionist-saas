import google.generativeai as genai
from typing import List, Dict, Any

from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

SYSTEM_PROMPT = """You are the AI front-desk assistant for {clinic_name}, a dental clinic.

Your job:
- Help patients book, reschedule, or cancel appointments
- Answer questions about services, pricing, and hours using ONLY the
  clinic's provided data — never invent prices or availability
- Collect basic intake info (name, phone, reason for visit) before booking
- Escalate to a human staff member for: medical advice, emergencies,
  complaints, or anything outside scheduling/FAQ scope
- Be warm, concise, and professional. Respond in the language the
  patient uses (English or Urdu).

Never diagnose, recommend treatment, or discuss clinical judgment —
you handle scheduling and information only. For emergencies, immediately
provide the clinic's emergency contact and tell the patient to call directly."""

TOOL_DEFINITIONS = [
    {
        "name": "check_availability",
        "description": "Get open appointment slots for a dentist/service in a date range",
        "parameters": {
            "type": "object",
            "properties": {
                "dentist_id": {"type": "string", "description": "Optional dentist ID"},
                "service_id": {"type": "string", "description": "Service ID"},
                "date_range_start": {"type": "string", "description": "ISO date string"},
                "date_range_end": {"type": "string", "description": "ISO date string"},
            },
            "required": ["service_id", "date_range_start", "date_range_end"],
        },
    },
    {
        "name": "book_appointment",
        "description": "Create a confirmed appointment for a patient",
        "parameters": {
            "type": "object",
            "properties": {
                "patient_phone": {"type": "string"},
                "patient_name": {"type": "string"},
                "service_id": {"type": "string"},
                "dentist_id": {"type": "string"},
                "start_time": {"type": "string", "description": "ISO datetime string"},
            },
            "required": [
                "patient_phone",
                "patient_name",
                "service_id",
                "dentist_id",
                "start_time",
            ],
        },
    },
    {
        "name": "reschedule_appointment",
        "description": "Move an existing appointment to a new time",
        "parameters": {
            "type": "object",
            "properties": {
                "appointment_id": {"type": "string"},
                "new_start_time": {"type": "string", "description": "ISO datetime string"},
            },
            "required": ["appointment_id", "new_start_time"],
        },
    },
    {
        "name": "cancel_appointment",
        "description": "Cancel an existing appointment",
        "parameters": {
            "type": "object",
            "properties": {
                "appointment_id": {"type": "string"},
                "reason": {"type": "string", "description": "Optional reason"},
            },
            "required": ["appointment_id"],
        },
    },
    {
        "name": "get_clinic_info",
        "description": "Fetch clinic hours, services, pricing, and location for FAQ answers",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "name": "escalate_to_staff",
        "description": "Flag conversation for human staff attention",
        "parameters": {
            "type": "object",
            "properties": {
                "conversation_id": {"type": "string"},
                "reason": {"type": "string"},
            },
            "required": ["conversation_id", "reason"],
        },
    },
]


async def get_gemini_response(
    clinic_name: str,
    conversation_history: List[Dict[str, str]],
    user_message: str,
) -> Dict[str, Any]:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT.format(clinic_name=clinic_name),
        tools=TOOL_DEFINITIONS,
    )

    chat = model.start_chat(history=[])

    for msg in conversation_history:
        if msg["role"] == "user":
            chat.history.append(genai.types.Content(role="user", parts=[msg["content"]]))
        else:
            chat.history.append(
                genai.types.Content(role="model", parts=[msg["content"]])
            )

    response = await chat.send_message_async(user_message)

    if response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if hasattr(part, "function_call") and part.function_call:
                return {
                    "type": "tool_call",
                    "tool_name": part.function_call.name,
                    "tool_args": dict(part.function_call.args),
                }

    return {
        "type": "text",
        "content": response.text,
    }
