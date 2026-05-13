"""
QualiOps API - Working version that definitely stays running
"""

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import uvicorn
import uuid
import subprocess
from datetime import datetime
import os

app = FastAPI()

# Simple storage
runs = {}

class TestRequest(BaseModel):
    test_name: str
    client_email: str

@app.get("/")
def home():
    return {
        "message": "QualiOps API is LIVE",
        "status": "operational",
        "time": datetime.now().isoformat()
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/run")
def start_test(request: TestRequest):
    run_id = str(uuid.uuid4())[:8]
    runs[run_id] = {
        "id": run_id,
        "status": "started",
        "test": request.test_name,
        "client": request.client_email
    }
    return {"run_id": run_id, "status": "started"}

@app.get("/status/{run_id}")
def get_run_status(run_id: str):
    return runs.get(run_id, {"error": "not found"})

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 QualiOps API Server - WORKING VERSION")
    print("="*60)
    print("Server starting at: http://localhost:8000")
    print("Press CTRL+C to stop")
    print("="*60 + "\n")
    
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8000,
        log_level="info",
        access_log=True
    )
