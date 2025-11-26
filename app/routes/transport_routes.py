from fastapi import APIRouter
from app.models import TransportRequest, TransportResponse
from app.helpers.transport_helper import calculate_transport_cost

router = APIRouter(prefix="/transport", tags=["Transport"])

@router.post("/calculate", response_model=TransportResponse)
def calculate(req: TransportRequest):
    total_cost, base_fare = calculate_transport_cost(
        req.route_name,
        req.distance_km,
        req.passengers
    )

    return TransportResponse(
        route_name=req.route_name,
        distance_km=req.distance_km,
        passengers=req.passengers,
        base_fare=base_fare,
        total_cost=total_cost
    )
