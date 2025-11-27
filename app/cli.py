#!/usr/bin/env python3

import requests
import os
import sys

BASE_URL = os.getenv("CT_BASE_URL", "http://127.0.0.1:8000") 

def fetch_stations():
    r = requests.get(f"{BASE_URL}/api/stations", timeout=5)
    r.raise_for_status()
    return r.json()

def fetch_buses():
    r = requests.get(f"{BASE_URL}/api/buses", timeout=5)
    r.raise_for_status()
    return r.json()

def choose_station(stations):
    print("\nAvailable stations:")
    for s in stations:
        print(f"{s['id']}: {s['name']} (lat={s['lat']}, lon={s['lon']})")
    while True:
        try:
            sid = int(input("Enter station id you want to go to (or 0 to choose nearest): ").strip())
            if sid == 0:
                return None
            if any(s['id'] == sid for s in stations):
                return sid
            print("Invalid station id, try again.")
        except ValueError:
            print("Please enter a number.")

def choose_bus(buses):
    print("\nAvailable buses:")
    for b in buses:
        print(f"{b['id']}: Route {b['route']} (heading to station {b['stop_id']})")
    while True:
        try:
            bid = int(input("Choose bus id you want to take: ").strip())
            if any(b['id'] == bid for b in buses):
                return bid
            print("Invalid bus id, try again.")
        except ValueError:
            print("Please enter a number.")

def parse_location_input():

    val = input("Enter your current location as 'lat,lon' (or press Enter to type them separately): ").strip()
    if val:
        try:
            lat_str, lon_str = val.split(",")
            lat = float(lat_str.strip())
            lon = float(lon_str.strip())
            return lat, lon
        except Exception:
            print("Invalid format. Please use e.g. -1.9577,30.0626")
    while True:
        try:
            lat = float(input("Enter latitude (e.g. -1.9577): ").strip())
            lon = float(input("Enter longitude (e.g. 30.0626): ").strip())
            return lat, lon
        except ValueError:
            print("Invalid numbers, try again.")

def find_nearest_station(user_lat, user_lon, stations):
    from math import radians, sin, cos, sqrt, atan2
    EARTH_KM = 6371.0
    def hav(lat1, lon1, lat2, lon2):
        rlat1, rlon1, rlat2, rlon2 = map(radians, (lat1, lon1, lat2, lon2))
        dlat = rlat2 - rlat1
        dlon = rlon2 - rlon1
        a = sin(dlat/2)**2 + cos(rlat1) * cos(rlat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        return EARTH_KM * c
    best = None
    best_d = 1e9
    for s in stations:
        d = hav(user_lat, user_lon, s['lat'], s['lon'])
        if d < best_d:
            best_d = d
            best = s
    return best

def main():
    print("Community Transport — CLI")
    try:
        stations = fetch_stations()
        buses = fetch_buses()
    except Exception as e:
        print("Error contacting backend API:", e)
        sys.exit(1)

    user_lat, user_lon = parse_location_input()

    sid = choose_station(stations)
    if sid is None:
        nearest = find_nearest_station(user_lat, user_lon, stations)
        sid = nearest['id']
        print(f"Nearest station is {nearest['name']} (id={sid})")

    bid = choose_bus(buses)

    try:
        r = requests.get(f"{BASE_URL}/api/eta", params={
            "user_lat": user_lat,
            "user_lon": user_lon,
            "station_id": sid,
            "bus_id": bid
        }, timeout=6)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print("Failed to get ETA:", e)
        sys.exit(1)

    print("\n--- Estimated Time Arrival ---")
    print(f"Station: {data['station_name']} (id {data['station_id']})")
    print(f"Distance you -> station: {data['distance_to_station_km']} km")
    print(f"Walking time: {data['walking_time_min']} minutes")
    print(f"Bus distance to station: {data['bus_distance_to_station_km']} km")
    print(f"Bus travel time (est): {data['bus_travel_time_min']} minutes")
    print(f"Traffic factor: {data['traffic_factor']}")
    print(f"Total ETA: {data['eta_minutes']} minutes")
    if data['should_wait']:
        print("Advice: You should wait for this bus.")
    else:
        print("Advice: Don't wait — consider another bus or transport method.")

if __name__ == "__main__":
    main()
