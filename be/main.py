from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from auth import router as auth_router
import httpx
import json
import os

app = FastAPI()
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
class AIRequest(BaseModel):
    messages: list[dict]
    model: str
    stream: bool = False


@app.get("/")
async def root():
    return FileResponse("public/index.html")


@app.get("/testai/")
async def testai():
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            res = await client.post(
                os.getenv("AI_URL"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {os.getenv("SECRET_KEY")}",
                },
                json={
                    "messages": [
                        {
                            "content": "You are a good personal assistant.",
                            "role": "system",
                        },
                        {"content": "What is the meaning of life?", "role": "user"},
                    ],
                    "model": "google/gemma-3-27b-instruct/bf-16",
                    "stream": False,
                },
            )
            res.raise_for_status()
            return res.json()
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Request to AI service timed out")
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=500, detail=f"Request to AI service failed: {exc}"
        )
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"External backend returned an error: {exc.response.text}",
        )
    except Exception as exc:
        raise HTTPException(status_code=00, detail=f"Unexpected error : {exc}")


@app.websocket("/teststream")
async def websocket_stream(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            user_message = await websocket.receive_text()

            async with httpx.AsyncClient() as client:
                res = await client.post(
                    os.getenv("AI_URL"),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {os.getenv("SECRET_KEY")}",
                    },
                    json={
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are a helpful assistant.",
                            },
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
                    if event.startswith("data:"):
                        data = event[5:].strip()

                        if data == "[DONE]" or not data:
                            await websocket.send_json(
                                {"type": "end", "data": "selesai bah"}
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
                                    await websocket.send_json(
                                        {"type": "content", "data": content}
                                    )
                        except json.JSONDecodeError:
                            continue

    except WebSocketDisconnect:
        print("Client disconnected")
    except httpx.RequestError as e:
        print(f"HTTP error: {str(e)}")
        try:
            await websocket.send_text(f"Error: {str(e)}")
        except:
            pass
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        try:
            await websocket.send_text(f"Unexpected error: {str(e)}")
        except:
            pass
    finally:
        try:
            if websocket.client_state.name != "DISCONNECTED":
                await websocket.close()
        except:
            pass


    
    
