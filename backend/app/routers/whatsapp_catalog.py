from fastapi import APIRouter
from pydantic import BaseModel
import httpx

from app.config import settings

router = APIRouter()


class CatalogItem(BaseModel):
    name: str
    description: str
    price: float
    image_url: str = None


@router.post("/catalog/sync")
async def sync_catalog_to_whatsapp(clinic_id: str, items: list[CatalogItem]):
    return {
        "status": "pending",
        "message": "WhatsApp catalog sync requires Meta Business API setup",
        "items_synced": len(items),
    }


@router.get("/catalog")
async def get_catalog(clinic_id: str):
    return {
        "catalog_id": None,
        "items": [],
        "message": "WhatsApp catalog not configured yet",
    }
