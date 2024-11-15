# server.py
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

# Allow Cross-Origin Requests (for front-end testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Active WebSocket connections
active_connections = {}

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()
    active_connections[username] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message["type"] == "offer":
                # Forward the offer to the target user
                receiver = message["receiver"]
                if receiver in active_connections:
                    await active_connections[receiver].send_text(json.dumps(message))
            
            elif message["type"] == "answer":
                # Forward the answer to the target user
                receiver = message["receiver"]
                if receiver in active_connections:
                    await active_connections[receiver].send_text(json.dumps(message))
            
            elif message["type"] == "candidate":
                # Forward the ICE candidate to the target user
                receiver = message["receiver"]
                if receiver in active_connections:
                    await active_connections[receiver].send_text(json.dumps(message))

    except WebSocketDisconnect:
        # Remove the connection when the user disconnects
        active_connections.pop(username, None)
