from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class TranslateRequest(BaseModel):
    text: str
    target_language: str = "ur"


TRANSLATIONS = {
    "greeting": {"en": "Hello! How can I help you?", "ur": "!خوش آمدید، میں آپ کی کیسے مدد کر سکتا ہوں"},
    "booking_confirmed": {"en": "Your appointment is confirmed.", "ur": "آپ کا ملاقات کی تائید ہو گئی ہے۔"},
    "emergency": {"en": "For emergencies, please call immediately.", "ur": "ہنگامی صورت میں، فوری طور پر کال کریں۔"},
    "goodbye": {"en": "Thank you for contacting us!", "ur": "ہم سے رابطہ کرنے کا شکریہ!"},
}


@router.post("/translate")
async def translate_message(data: TranslateRequest):
    return {
        "original": data.text,
        "translated": data.text,
        "target_language": data.target_language,
        "message": "Translation requires external API integration",
    }


@router.get("/greetings")
async def get_greetings():
    return TRANSLATIONS
