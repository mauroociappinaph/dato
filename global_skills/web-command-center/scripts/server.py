import os
import json
import re
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import asyncio

app = FastAPI(title="The Dude Web Command Center Backend")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

PROJECT_ROOT = Path("/Users/mauroociappina/.gemini")
LOGS_DIR = PROJECT_ROOT / "logs"
WORKSPACE_DIR = PROJECT_ROOT / "workspace"

@app.get("/")
async def get_dashboard():
    html_path = WORKSPACE_DIR / "dude-command-center.html"
    if html_path.exists():
        return FileResponse(html_path)
    return {"error": "Dashboard HTML not found. Run generate_ui.py first."}

@app.get("/api/health")
async def health_check():
    return {"status": "operational", "version": "7.0", "engine": "FastAPI"}

@app.get("/api/logs/summary")
async def get_logs_summary():
    summary = []
    for log_file in LOGS_DIR.glob("*.log"):
        try:
            # Get last 5 lines
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()[-5:]
            summary.append({
                "file": log_file.name,
                "last_update": os.path.getmtime(log_file),
                "preview": "".join(lines)
            })
        except Exception:
            continue
    return summary

@app.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("🚀 Command Center: WebSocket Connected.")
    try:
        while True:
            # Tail logs and send updates
            # For now, just a heartbeat every 5s
            summary = await get_logs_summary()
            await websocket.send_json({"type": "LOG_UPDATE", "data": summary})
            await asyncio.sleep(5)
    except Exception as e:
        print(f"❌ WebSocket Disconnected: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
