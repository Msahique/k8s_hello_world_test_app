from fastapi import FastAPI
from datetime import datetime
import socket

app = FastAPI(title="App2", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok", "app": "app2"}


@app.get("/info")
def info():
    return {
        "app":        "app2",
        "server":     socket.gethostname(),
        "timestamp":  datetime.utcnow().isoformat() + "Z",
    }
