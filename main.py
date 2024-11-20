from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List, Dict

app = FastAPI()

# Store connections by room_id (shared chat room ID)
active_connections: Dict[str, List[WebSocket]] = {}

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    # Accept the WebSocket connection
    await websocket.accept()

    # Add the connection to the list for the specified room_id
    if room_id not in active_connections:
        active_connections[room_id] = []
    active_connections[room_id].append(websocket)

    try:
        while True:
            # Wait for a message from the user
            message = await websocket.receive_text()

            # Broadcast the message to all other users in the same room_id
            for connection in active_connections[room_id]:
                if connection != websocket:
                    await connection.send_text(message)
    except WebSocketDisconnect:
        # Remove the connection when disconnected
        active_connections[room_id].remove(websocket)
        if not active_connections[room_id]:
            del active_connections[room_id]
        await websocket.close()
