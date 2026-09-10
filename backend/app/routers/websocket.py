from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.websocket_manager import manager

router = APIRouter()


@router.websocket("/ws/{clinic_id}")
async def websocket_endpoint(websocket: WebSocket, clinic_id: str):
    await manager.connect(websocket, clinic_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_to_clinic(clinic_id, {"type": "message", "data": data})
    except WebSocketDisconnect:
        manager.disconnect(websocket, clinic_id)
