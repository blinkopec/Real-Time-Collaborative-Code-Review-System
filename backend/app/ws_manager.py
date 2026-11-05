from collections import defaultdict

from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect


class ConnectionManager:
    def __init__(self):
        self.rooms: dict[int, set[WebSocket]] = defaultdict(set)

    async def connect(self, room_id: int, ws: WebSocket):
        await ws.accept()
        self.rooms[room_id].add(ws)

    def disconnect(self, room_id: int, ws: WebSocket):
        self.rooms[room_id].discard(ws)
        if not self.rooms[room_id]:
            self.rooms.pop(room_id, None)

    async def broadcast(self, room_id: int, message: dict):
        dead_connections = []

        for ws in self.rooms.get(room_id, set()):
            try:
                await ws.send_json(message)
            except (WebSocketDisconnect, RuntimeError):
                dead_connections.append(ws)

        for ws in dead_connections:
            self.disconnect(room_id, ws)


manager = ConnectionManager()
