from math import radians, sin, cos, sqrt, atan2, ceil
import time
from typing import Optional, Tuple, List
from ..database import STATIONS, BUSES
from ..models import Station, Bus

EARTH_KM = 6371.0
# this returns distance in kilmeters 
def haversine(lat1, lon1, lat2, lon2):
    rlat1, rlon1, rlat2, rlon2 = map(radians, (lat1, lon1, lat2, lon2))
    dlat = rlat2 - rlat1
    dlon = rlon2 - rlon1
    a = sin(dlat/2)**2 + cos(rlat1) * cos(rlat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return EARTH_KM * c

def get_all_stations() -> List[Station]:
    return [Station(**s) for s in STATIONS]

def get_station_by_id(station_id: int) -> Optional[Station]:
    for s in STATIONS:
        if s["id"] == station_id:
            return Station(**s)
    return None

def get_all_buses() -> List[Bus]:
    return [Bus(**b) for b in BUSES]

def get_bus_by_id(bus_id: int) -> Optional[Bus]:
    for b in BUSES:
        if b["id"] == bus_id:
            return Bus(**b)
    return None

def estimate_eta(user_lat: float, user_lon: float, station_id: int, bus_id: int) -> dict:
    station = get_station_by_id(station_id)
    if not station:
        raise ValueError("Station not found")

    bus = get_bus_by_id(bus_id)
    if not bus:
        raise ValueError("Bus not found")

    distance_user_station_km = haversine(user_lat, user_lon, station.lat, station.lon)

    walking_time_hr = distance_user_station_km / 5.0
    walking_time_min = ceil(walking_time_hr * 60)

    distance_bus_station_km = haversine(bus.current_lat, bus.current_lon, station.lat, station.lon)

    hour = time.localtime().tm_hour
    if 7 <= hour <= 9 or 16 <= hour <= 19:
        traffic_factor = 1.4  
    else:
        traffic_factor = 1.0 

    bus_travel_time_min = ceil((distance_bus_station_km / bus.speed_kmph) * 60 * traffic_factor)


    eta_minutes = walking_time_min + bus_travel_time_min

    should_wait = eta_minutes <= 15

    return {
        "user_lat": user_lat,
        "user_lon": user_lon,
        "station_id": station.id,
        "station_name": station.name,
        "distance_to_station_km": round(distance_user_station_km, 3),
        "walking_time_min": walking_time_min,
        "bus_distance_to_station_km": round(distance_bus_station_km, 3),
        "bus_travel_time_min": bus_travel_time_min,
        "traffic_factor": traffic_factor,
        "eta_minutes": eta_minutes,
        "should_wait": should_wait
    }
