# app/main.py
import socket
from fastapi import FastAPI
from app.routes.transport_routes import router as transport_router

app = FastAPI(title="Community Transport Service API")
app.include_router(transport_router, prefix="/transport")

@app.get("/")
def home():
    return {"message": "Community Transport API is running", "server": socket.gethostname()}
