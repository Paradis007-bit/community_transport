from pydantic import BaseModel
from typing import Optional

class Station(BaseModel):
    id: int
    name: str
    lat: float
    lon: float

class Bus(BaseModel):
    id: int
    route: str
    current_lat: float
    current_lon: float
    speed_kmph: float  # average speed
    stop_id: int       # station id the bus is heading to

class ETAResponse(BaseModel):
    user_lat: float
    user_lon: float
    station_id: int
    station_name: str
    distance_to_station_km: float
    walking_time_min: int
    bus_distance_to_station_km: float
    bus_travel_time_min: int
    traffic_factor: float
    eta_minutes: int
    should_wait: bool
