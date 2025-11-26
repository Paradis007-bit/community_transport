from pydantic import BaseModel

class TransportRequest(BaseModel):
    distance_km: float
    passengers: int
    route_name: str

class TransportResponse(BaseModel):
    route_name: str
    distance_km: float
    passengers: int
    base_fare: float
    total_cost: float
