import os
import json
import logging
from typing import Dict, Any, List
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("SprinklerController")

app = FastAPI(title="SprinklerController-io")

# Setup template engine
templates = Jinja2Templates(directory="/app/templates")

# Mock/Initial State
state = {
    "system_name": "SprinklerController-io",
    "status": "idle",  # idle, watering, rain_delay, freeze_lockout
    "weather": {
        "temperature_c": 21.5,
        "rain_detected": False,
        "rain_delay_active": False,
        "freeze_lockout_active": False,
        "et_rate_mm_day": 4.2
    },
    "zones": [
        {
            "id": 1,
            "name": "Front Lawn",
            "state": "idle",
            "default_duration_min": 15,
            "cycle_count": 2,
            "soak_minutes": 10,
            "flow_rate_gpm": 4.5,
            "node_type": "ESP32 (WT32-ETH01 Ethernet)",
            "soil_moisture_pct": 38.0
        },
        {
            "id": 2,
            "name": "Back Lawn",
            "state": "idle",
            "default_duration_min": 20,
            "cycle_count": 2,
            "soak_minutes": 15,
            "flow_rate_gpm": 5.0,
            "node_type": "ESP32 (Wi-Fi 8-Relay)",
            "soil_moisture_pct": 42.0
        },
        {
            "id": 3,
            "name": "Garden Beds",
            "state": "idle",
            "default_duration_min": 10,
            "cycle_count": 1,
            "soak_minutes": 0,
            "flow_rate_gpm": 2.0,
            "node_type": "ESP32 (Wi-Fi + BLE Gateway)",
            "soil_moisture_pct": 55.0
        },
        {
            "id": 4,
            "name": "Shrubs & Planters",
            "state": "idle",
            "default_duration_min": 12,
            "cycle_count": 1,
            "soak_minutes": 0,
            "flow_rate_gpm": 2.2,
            "node_type": "ESP32 (Wi-Fi 8-Relay)",
            "soil_moisture_pct": 49.0
        }
    ],
    "flow": {
        "current_gpm": 0.0,
        "daily_gallons": 142.0,
        "leak_detected": False
    }
}

class ZoneAction(BaseModel):
    duration_minutes: int = 10

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "state": state})

@app.get("/api/state")
async def get_state():
    return state

@app.post("/api/zones/{zone_id}/run")
async def run_zone(zone_id: int, action: ZoneAction):
    for zone in state["zones"]:
        if zone["id"] == zone_id:
            zone["state"] = "watering"
            state["status"] = "watering"
            state["flow"]["current_gpm"] = zone["flow_rate_gpm"]
            logger.info(f"Started watering zone {zone['name']} for {action.duration_minutes}m")
            return {"status": "ok", "zone": zone}
    return JSONResponse(status_code=404, content={"error": "Zone not found"})

@app.post("/api/zones/{zone_id}/stop")
async def stop_zone(zone_id: int):
    for zone in state["zones"]:
        if zone["id"] == zone_id:
            zone["state"] = "idle"
            logger.info(f"Stopped watering zone {zone['name']}")
    
    # Check if any zone is still running
    if not any(z["state"] == "watering" for z in state["zones"]):
        state["status"] = "idle"
        state["flow"]["current_gpm"] = 0.0
        
    return {"status": "ok"}

@app.post("/api/system/stop_all")
async def stop_all():
    for zone in state["zones"]:
        zone["state"] = "idle"
    state["status"] = "idle"
    state["flow"]["current_gpm"] = 0.0
    logger.info("Emergency Stop / Stop All triggered")
    return {"status": "ok", "message": "All zones shut off"}
