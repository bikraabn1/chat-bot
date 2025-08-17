from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from auth import router as auth_router
import socketio
import httpx
import json
import os

sio = socketio.AsyncServer(cors_allowed_origins=["*"], async_mode="asgi")
fast_api_app = FastAPI()

fast_api_app.add_middleware(
    CORSMiddleware,
    allow_origin=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

fast_api_app.include_router(auth_router)


@fast_api_app.get("/")
async def root():
    return FileResponse("public/index.html")


@sio.event
async def connect(sid, environ):
    print(f"Client connected : {sid}")


@sio.event
async def disconnect(sid):
    print(f"Client disconnected : {sid}")


@sio.event
async def user_prompt(sid, data):
    user_message = data.get("message", "")

    async with httpx.AsyncClient() as client:
        res = await client.post(
            os.getenv("AI_URL"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {os.getenv("AI_SECRET_KEY")}",
            },
            json={
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message},
                ],
                "model": "google/gemma-3-27b-instruct/bf-16",
                "stream": True,
            },
            timeout=30.0,
        )

        res.raise_for_status()

        buffer = ""

        async for chunk in res.aiter_text():
            buffer += chunk

            while "\n\n" in buffer:
                event, buffer = buffer.split("\n\n", 1)
                if event.startswith("data: "):
                    data = event[5:].strip()

                    if data == "DONE" or not data:
                        await sio.emit(
                            "stream_end", {"data": "stream was ended"}, to=sid
                        )
                        continue

                    try:
                        payload = json.loads(data)
                        if "choices" in payload and payload["choices"]:
                            content = (
                                payload["choices"][0]
                                .get("delta", {})
                                .get("content", "")
                            )
                            if content:
                                await sio.emit(
                                    "stream_chunk", {"data": content}, to=sid
                                )

                    except json.JSONDecodeError:
                        continue


app = socketio.ASGIApp(sio, other_asgi_app=fast_api_app, socketio_path="/ai")
