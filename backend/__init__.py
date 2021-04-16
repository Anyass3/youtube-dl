
from fastapi import FastAPI, Path, Query
from starlette.websockets import WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from backend import socket, routes

app = FastAPI()

app.include_router(routes.router)
app.include_router(socket.router)

# replace these with yours
origins = [
    "http://localhost:3000",
    "http://localhost:5000",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:7777",
    "https://youtube-d.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
