from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect

from app.security import decode_access_token
from app.ws_manager import manager

router = APIRouter(tags=["ws"])


@router.websocket("/ws/rooms/{snippet_id}")
async def ws_room(websocket: WebSocket, snippet_id: int, token: str = Query(...)):
    user_id = decode_access_token(token)

    if user_id is None:
        await websocket.close(code=4401)
        return

    await manager.connect(snippet_id, websocket)
    await manager.broadcast(
        snippet_id,
        {"type": "presence", "data": {"user_id": int(user_id), "event": "join"}},
    )

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(snippet_id, websocket)
        await manager.broadcast(
            snippet_id,
            {
                "type": "presence",
                "data": {"user_id": int(user_id), "event": "leave"},
            },
        )
