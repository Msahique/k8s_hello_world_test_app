from fastapi import FastAPI
from datetime import datetime
import socket
import httpx

app = FastAPI(title="App1", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok", "app": "app1"}


@app.get("/info")
def info():
    return {
        "app":        "app1",
        "server":     socket.gethostname(),
        "timestamp":  datetime.utcnow().isoformat() + "Z",
    }

@app.get("/call1-app2-info")
async def call1_app2_info():
    """Call app2's /info endpoint from app1"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://app2-svc:80/info",
            timeout=10.0
        )
        app2_data = response.json()
    
    return {
        "app": "app1",
        "called_app2": app2_data,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@app.get("/call2-app2-info")
async def call2_app2_info():
    """Call app2's /info endpoint from app1"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://app2-svc/info",
            timeout=10.0
        )
        app2_data = response.json()
    
    return {
        "app": "app1",
        "called_app2": app2_data,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }