import os
import requests
import time
import datetime
from config import (
    BASE_URL, HEADERS, BOUNDS, CHECK_INTERVAL, SCREENSHOT_COOLDOWN,
    JUANDA_LAT, JUANDA_LON, JUANDA_ZOOM
)
from detector import (
    update_aircraft, detect_holding, can_take_screenshot, 
    update_screenshot_time, get_aircraft_info
)
from screenshot import take_screenshot


def system_on():
    """Cek apakah sistem dalam keadaan ON"""
    try:
        with open("mode.txt") as f:
            return f.read().strip() == "ON"
    except:
        return False


def log_event(message):
    """Log events ke file CSV"""
    os.makedirs("logs", exist_ok=True)
    with open("logs/events.csv", "a") as f:
        f.write(f"{datetime.datetime.now().isoformat()},{message}\n")




def fetch_flights():
    """Fetch real flight data from FlightRadar24 API"""
    try:
        response = requests.get(
            f"{BASE_URL}?bounds={BOUNDS}",
            headers=HEADERS,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("aircraft", [])
        else:
            print(f"[API ERROR] Status: {response.status_code}")
            return []
    except Exception as e:
        print(f"[API ERROR] {e}")
        return []


def process_flights():
    """Process flights from API and detect holding pattern"""
    flights = fetch_flights()
    
    if not flights:
        print("[INFO] No flights found")
        return None
    
    print(f"[API] Found {len(flights)} flights")
    
    holding_detected_flight = None
    
    for flight in flights:
        icao = flight.get("icao24")
        callsign = flight.get("callsign", "").strip()
        lat = flight.get("lat")
        lon = flight.get("lon")
        track = flight.get("track")
        
        # Skip jika tidak ada callsign atau track
        if not callsign or track is None:
            continue
        
        # Update aircraft history
        update_aircraft(flight)
        
        # Get aircraft info for debugging
        info = get_aircraft_info(icao)
        if info and info["data_points"] >= 5:
            print(f"  {callsign}: {info['data_points']} points, heading change: {info['total_heading_change']:.1f}°")
        
        # Check if holding pattern detected
        if detect_holding(icao):
            print(f"[HOLDING DETECTED] {callsign} (ICAO: {icao})")
            holding_detected_flight = {
                "callsign": callsign,
                "icao": icao,
                "lat": lat,
                "lon": lon,
                "track": track
            }
            break
    
    return holding_detected_flight


# Main program
if __name__ == "__main__":
    print("=" * 60)
    print("AUTO SCREENSHOT FLIGHTRADAR24 - HOLDING DETECTOR")
    print("=" * 60)
    print(f"Area: Bandar Udara Internasional Juanda")
    print(f"Center: {JUANDA_LAT}, {JUANDA_LON}")
    print(f"Zoom Level: {JUANDA_ZOOM}")
    print(f"Bounding Box: {BOUNDS}")
    print(f"Check Interval: {CHECK_INTERVAL}s")
    print(f"Screenshot Cooldown: {SCREENSHOT_COOLDOWN}s ({SCREENSHOT_COOLDOWN//60} menit)")
    print("=" * 60)
    print("Tekan Ctrl+C untuk menghentikan")
    print("=" * 60)

    while True:
        if not system_on():
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] System OFF - Set mode.txt to ON to start")
            time.sleep(5)
            continue

        print(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] Checking flights...")
        
        holding_flight = process_flights()
        
        if holding_flight:
            callsign = holding_flight["callsign"]
            icao = holding_flight["icao"]
            
            print(f"[HOLDING] {callsign} detected at position {holding_flight['lat']}, {holding_flight['lon']}")
            
            # Cek cooldown sebelum screenshot
            if can_take_screenshot(icao):
                print(f"[SCREENSHOT] Taking screenshot for {callsign}...")
                take_screenshot(callsign)
                
                # Update screenshot time
                update_screenshot_time(icao)
                
                # Log event
                log_event(f"HOLDING_DETECTED,{callsign},{icao},{holding_flight['lat']},{holding_flight['lon']}")
                
                print(f"[COOLDOWN] Waiting {SCREENSHOT_COOLDOWN}s ({SCREENSHOT_COOLDOWN//60} menit) before next check...")
                time.sleep(SCREENSHOT_COOLDOWN)
            else:
                print(f"[COOLDOWN] Screenshot for {callsign} already taken recently, skipping...")
                time.sleep(CHECK_INTERVAL)
        else:
            print("[INFO] No holding pattern detected")
            time.sleep(CHECK_INTERVAL)
