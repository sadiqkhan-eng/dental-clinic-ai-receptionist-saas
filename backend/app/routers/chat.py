from fastapi import APIRouter
from pydantic import BaseModel

from app.services.chat_service import handle_incoming_message

router = APIRouter()


class ChatRequest(BaseModel):
    clinic_slug: str
    message: str
    channel: str = "web"
    phone_number: str = None


@router.post("/chat")
async def chat(request: ChatRequest):
    phone = request.phone_number or f"web_user_{id(request)}"

    await handle_incoming_message(
        channel=request.channel,
        phone_number=phone,
        message_text=request.message,
        clinic_slug=request.clinic_slug,
    )

    return {"reply": "Your message has been received. An AI assistant will respond shortly."}
