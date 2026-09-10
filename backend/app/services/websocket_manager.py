from typing import Dict, Set
from fastapi import WebSocket
import json


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, clinic_id: str):
        await websocket.accept()
        if clinic_id not in self.active_connections:
            self.active_connections[clinic_id] = set()
        self.active_connections[clinic_id].add(websocket)

    def disconnect(self, websocket: WebSocket, clinic_id: str):
        if clinic_id in self.active_connections:
            self.active_connections[clinic_id].discard(websocket)

    async def send_to_clinic(self, clinic_id: str, message: dict):
        if clinic_id in self.active_connections:
            for connection in self.active_connections[clinic_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    pass

    async def broadcast(self, message: dict):
        for clinic_id in self.active_connections:
            await self.send_to_clinic(clinic_id, message)


manager = ConnectionManager()
