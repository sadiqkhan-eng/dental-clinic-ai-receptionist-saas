from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from app.database import get_db
from app.config import settings

router = APIRouter()


class RoomCreate(BaseModel):
    clinic_id: str
    patient_id: str
    appointment_id: str


@router.post("/room")
async def create_video_room(data: RoomCreate):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.daily.co/v1/rooms",
                headers={"Authorization": f"Bearer {settings.DAILY_API_KEY}"},
                json={
                    "properties": {
                        "enable_chat": True,
                        "enable_screen_sharing": True,
                        "enable_recording": "cloud",
                    }
                },
            )
            room = response.json()
            return {
                "room_url": room.get("url"),
                "room_name": room.get("name"),
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/room/{room_name}")
async def get_room_token(room_name: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://api.daily.co/v1/meeting-tokens",
                headers={"Authorization": f"Bearer {settings.DAILY_API_KEY}"},
                json={
                    "room_name": room_name,
                    "is_owner": False,
                },
            )
            data = response.json()
            return {"token": data.get("token")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
