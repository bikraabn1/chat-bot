from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from settings import Settings
from pydantic import BaseModel
import httpx
import json

settings = Settings()

app = FastAPI()

class AIRequest(BaseModel):
    messages: list[dict]
    model:str
    stream: bool = False

@app.get("/")
async def root():
    return FileResponse("public/index.html")
    
@app.get("/testai/")
async def testai():
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            res = await client.post(
                settings.ai_url,
                headers={
                    "Content-Type" : "application/json",
                    "Authorization" : f"Bearer {settings.secret_key.get_secret_value()}"
                },json= {
                    "messages": [
                        {
                            "content": "You are a good personal assistant.",
                            "role": "system"
                        },
                        {
                            "content": "What is the meaning of life?",
                            "role": "user"
                        }
                    ],
                    "model": "google/gemma-3-27b-instruct/bf-16",
                    "stream": False
                }
            )
            res.raise_for_status()
            return res.json()
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Request to AI service timed out"
        )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=500, 
            detail=f"Request to AI service failed: {exc}"
        )
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"External backend returned an error: {exc.response.text}"
        )
    except Exception as exc:
        raise HTTPException(
            status_code=00,
            detail=f"Unexpected error : {exc}"
        )
    
@app.websocket('/teststream')
async def websocket_stream(websocket: WebSocket):
    await websocket.accept()

    try :
        while True :
            user_message = await websocket.receive_text()
            
            async with httpx.AsyncClient() as client:
                res = await client.post(
                    settings.ai_url,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {settings.secret_key.get_secret_value()}"
                    },
                    json={
                        "messages": [
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": user_message}
                        ],
                        "model": "google/gemma-3-27b-instruct/bf-16",
                        "stream": True  
                    },
                    timeout=30.0
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
                            await websocket.send_json({"type" : "end", "data" : "selesai bah"})
                            continue
                                
                        try:
                            payload = json.loads(data)
                            if "choices" in payload and payload["choices"]:
                                content = payload["choices"][0].get("delta", {}).get("content", "")
                                if content:
                                    await websocket.send_json({ "type" : "content", "data" : content}) 
                        except json.JSONDecodeError:
                            continue

    except WebSocketDisconnect:
        print("Client disconnected")
    except httpx.RequestError as e:
        await websocket.send_text(f"Error: {str(e)}")
    except Exception as e:
        await websocket.send_text(f"Unexpected error: {str(e)}")
    finally:
        await websocket.close()  