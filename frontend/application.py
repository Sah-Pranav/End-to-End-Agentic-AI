import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
import httpx
import os
import json

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Serve static files (css, js)
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
async def read_index():
    return FileResponse("index.html")

@app.get("/{filename}")
async def read_file(filename: str):
    if os.path.exists(filename):
        return FileResponse(filename)
    return {"error": "File not found"}

class QueryRequest(BaseModel):
    question: str
    thread_id: str = "default_thread"

@app.post("/chat/stream")
async def proxy_chat_stream(query: QueryRequest):
    logger.info(f"Received proxy request for: {query.question}")
    # Proxy the request to the backend (main.py running on port 8000)
    backend_url = "http://127.0.0.1:8000/chat/stream"
    logger.info(f"Connecting to backend: {backend_url}")
    
    async def stream_proxy():
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream("POST", backend_url, json=query.model_dump(), timeout=None) as response:
                    logger.info(f"Backend status: {response.status_code}")
                    async for chunk in response.aiter_bytes():
                        logger.info(f"Yielding chunk of size: {len(chunk)}")
                        if len(chunk) > 0:
                            logger.info(f"Chunk content (first 50): {chunk[:50]}")
                        yield chunk
        except Exception as e:
            logger.error(f"Proxy error: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n".encode()

    return StreamingResponse(stream_proxy(), media_type="text/event-stream")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
