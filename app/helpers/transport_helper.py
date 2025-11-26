from app.database import TRANSPORT_ROUTES

def calculate_transport_cost(route_name: str, distance_km: float, passengers: int):
    if route_name not in TRANSPORT_ROUTES:
        raise ValueError("Unknown route")

    base_fare = TRANSPORT_ROUTES[route_name]["base_fare"]

    distance_cost = distance_km * 250      # fixed cost per km
    passenger_cost = passengers * 100      # fixed cost per passenger

    total = base_fare + distance_cost + passenger_cost
    return round(total, 2), base_fare
