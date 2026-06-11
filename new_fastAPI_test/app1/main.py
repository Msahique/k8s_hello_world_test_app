from fastapi import FastAPI
from datetime import datetime
import socket

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
