from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.cache import cache_close
from app.services.rate_limiter import RateLimitMiddleware
from app.services.websocket_manager import manager
from app.routers import (
    clinics, patients, services, appointments,
    chat, webhooks, billing, dentists, conversations, staff,
    waiting_list, referrals, invoices, analytics, telemedicine,
    training, packages, insurance, whitelabel, api_access,
    marketplace, multilang, whatsapp_catalog,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await cache_close()

app = FastAPI(
    title="DentalOS API",
    description="AI-Powered Dental Clinic SaaS Backend",
    version="0.3.0",
    lifespan=lifespan,
)

app.add_middleware(RateLimitMiddleware, requests_per_minute=100)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clinics.router, prefix="/api/clinics", tags=["clinics"])
app.include_router(patients.router, prefix="/api/patients", tags=["patients"])
app.include_router(services.router, prefix="/api/services", tags=["services"])
app.include_router(dentists.router, prefix="/api/dentists", tags=["dentists"])
app.include_router(appointments.router, prefix="/api/appointments", tags=["appointments"])
app.include_router(conversations.router, prefix="/api/conversations", tags=["conversations"])
app.include_router(staff.router, prefix="/api/staff", tags=["staff"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
app.include_router(billing.router, prefix="/api/billing", tags=["billing"])
app.include_router(waiting_list.router, prefix="/api/waiting-list", tags=["waiting-list"])
app.include_router(referrals.router, prefix="/api/referrals", tags=["referrals"])
app.include_router(invoices.router, prefix="/api/invoices", tags=["invoices"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(telemedicine.router, prefix="/api/telemedicine", tags=["telemedicine"])
app.include_router(training.router, prefix="/api/training", tags=["training"])
app.include_router(packages.router, prefix="/api/packages", tags=["packages"])
app.include_router(insurance.router, prefix="/api/insurance", tags=["insurance"])
app.include_router(whitelabel.router, prefix="/api/whitelabel", tags=["whitelabel"])
app.include_router(api_access.router, prefix="/api/access", tags=["api-access"])
app.include_router(marketplace.router, prefix="/api/marketplace", tags=["marketplace"])
app.include_router(multilang.router, prefix="/api/multilang", tags=["multilang"])
app.include_router(whatsapp_catalog.router, prefix="/api/whatsapp", tags=["whatsapp-catalog"])


@app.websocket("/ws/{clinic_id}")
async def websocket_endpoint(websocket: WebSocket, clinic_id: str):
    await manager.connect(websocket, clinic_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_to_clinic(clinic_id, {"type": "message", "data": data})
    except Exception:
        manager.disconnect(websocket, clinic_id)


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.3.0"}
