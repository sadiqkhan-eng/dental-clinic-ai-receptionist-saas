from fastapi import APIRouter, Request, Response
from app.config import settings

router = APIRouter()


@router.get("/whatsapp")
async def verify_whatsapp_webhook(
    hub_mode: str = None,
    hub_verify_token: str = None,
    hub_challenge: str = None,
):
    if hub_mode == "subscribe" and hub_verify_token == settings.WHATSAPP_VERIFY_TOKEN:
        return Response(content=hub_challenge, media_type="text/plain")
    return Response(status_code=403)


@router.post("/whatsapp")
async def receive_whatsapp_message(request: Request):
    payload = await request.json()

    entry = payload.get("entry", [{}])[0]
    changes = entry.get("changes", [{}])[0]
    value = changes.get("value", {})

    messages = value.get("messages", [])
    if not messages:
        return {"status": "ok"}

    message = messages[0]
    phone = message.get("from")
    text = message.get("text", {}).get("body", "")

    from app.services.chat_service import handle_incoming_message

    await handle_incoming_message(
        channel="whatsapp",
        phone_number=phone,
        message_text=text,
    )

    return {"status": "ok"}
