from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from auth import router as auth_router
from upload import router as upload_router
import socketio
import httpx
import json
import os

sio = socketio.AsyncServer(
    cors_allowed_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    async_mode="asgi",
    logger=True,
    engineio_logger=True
)

fast_api_app = FastAPI()

fast_api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

fast_api_app.include_router(auth_router)
fast_api_app.include_router(upload_router)

@fast_api_app.get("/")
async def root():
    return {"message": "server started"}

@sio.event(namespace='/')
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    print(f"Environment: {environ}")
    await sio.emit('connect_response', {'status': 'connected', 'sid': sid}, to=sid, namespace='/')

@sio.event(namespace='/')
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.event(namespace='/')
async def user_prompt(sid, data):
    user_message = data.get("message", "")
    print(f"Received message: {user_message}")

    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                os.getenv("AI_URL"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {os.getenv('AI_SECRET_KEY')}",
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
            chunk_count = 0

            async for chunk in res.aiter_text():
                chunk_count += 1
                print(f"Raw chunk {chunk_count}: {repr(chunk)}")  # Debug raw chunks
                buffer += chunk

                while "\n\n" in buffer:
                    event, buffer = buffer.split("\n\n", 1)
                    print(f"Processing event: {repr(event)}")  # Debug events
                    
                    if event.startswith("data: "):
                        data_content = event[5:].strip()
                        print(f"Data content: {repr(data_content)}")  # Debug data

                        if data_content == "DONE" or data_content == "[DONE]" or not data_content:
                            print("Stream ended - sending stream_end")
                            await sio.emit(
                                "stream_end", {"data": "stream was ended"}, to=sid, namespace='/'
                            )
                            continue

                        try:
                            payload = json.loads(data_content)
                            print(f"Parsed payload: {payload}")  # Debug parsed JSON
                            
                            if "choices" in payload and payload["choices"]:
                                content = (
                                    payload["choices"][0]
                                    .get("delta", {})
                                    .get("content", "")
                                )
                                if content:
                                    print(f"Sending content: {repr(content)}")
                                    await sio.emit(
                                        "stream_chunk", {"data": content}, to=sid, namespace='/'
                                    )

                        except json.JSONDecodeError as e:
                            print(f"JSON decode error: {e} for data: {repr(data_content)}")
                            continue
                            
            print("All chunks processed - sending final stream_end")
            await sio.emit("stream_end", {"data": "stream completed"}, to=sid, namespace='/')

    except Exception as e:
        print(f"Error: {e}")
        await sio.emit("error", {"message": str(e)}, to=sid, namespace='/')

app = socketio.ASGIApp(sio, other_asgi_app=fast_api_app)