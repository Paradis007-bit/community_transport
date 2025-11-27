from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from ..helpers.transport_helper import get_all_stations, get_all_buses, estimate_eta, get_station_by_id
from ..models import Station, Bus, ETAResponse

router = APIRouter(prefix="/api")

@router.get("/status")
def status():
    return {"service": "community_transport", "status": "running"}

@router.get("/stations", response_model=List[Station])
def stations():
    return get_all_stations()

@router.get("/buses", response_model=List[Bus])
def buses():
    return get_all_buses()

@router.get("/eta", response_model=ETAResponse)
def eta(
    user_lat: float = Query(..., description="Your latitude"),
    user_lon: float = Query(..., description="Your longitude"),
    station_id: int = Query(..., description="Station id to meet the bus"),
    bus_id: int = Query(..., description="Bus id")
):
    try:
        data = estimate_eta(user_lat, user_lon, station_id, bus_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return ETAResponse(**data)
