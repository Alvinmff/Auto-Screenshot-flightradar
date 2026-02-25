import math
from collections import defaultdict
from datetime import datetime, timedelta

# Dictionary untuk menyimpan history heading setiap pesawat
aircraft_history = defaultdict(list)

# Dictionary untuk menyimpan waktu screenshot terakhir
last_screenshot_time = {}

# Minimum data points untuk mendeteksi holding
MIN_HISTORY_POINTS = 5

# Threshold total perubahan heading untuk holding pattern (dalam derajat)
HOLDING_HEADING_THRESHOLD = 300

# Cooldown dalam detik (sama dengan SCREENSHOT_COOLDOWN di config)
SCREENSHOT_COOLDOWN = 900  # 15 menit


def calculate_heading_change(history):
    """
    Hitung total perubahan heading dari history
    Menghitung perbedaan antara heading consecutive
    dan handle wrap-around (360 -> 0)
    """
    if len(history) < MIN_HISTORY_POINTS:
        return 0
    
    total_change = 0
    for i in range(1, len(history)):
        diff = abs(history[i] - history[i-1])
        # Handle wrap-around: jika perubahan > 180, ambil arah sebaliknya
        total_change += min(diff, 360 - diff)
    
    return total_change


def update_aircraft(flight):
    """
    Update history heading untuk sebuah pesawat
    Returns icao24 jika berhasil diupdate, None jika gagal
    """
    icao = flight.get("icao24")
    heading = flight.get("track")

    if icao and heading is not None:
        # Append heading ke history
        aircraft_history[icao].append(heading)

        # Keep only last 20 data points
        if len(aircraft_history[icao]) > 20:
            aircraft_history[icao].pop(0)

        return icao

    return None


def detect_holding(icao):
    """
    Deteksi apakah pesawat sedang dalam holding pattern
    Berdasarkan total perubahan heading > threshold
    """
    if icao not in aircraft_history:
        return False
    
    history = aircraft_history[icao]
    total_heading = calculate_heading_change(history)

    if total_heading > HOLDING_HEADING_THRESHOLD:
        return True

    return False


def can_take_screenshot(icao):
    """
    Cek apakah boleh mengambil screenshot berdasarkan cooldown
    Returns True jika boleh, False jika masih dalam cooldown
    """
    current_time = datetime.now()
    
    if icao not in last_screenshot_time:
        # Belum pernah screenshot, boleh ambil
        return True
    
    last_time = last_screenshot_time[icao]
    elapsed = (current_time - last_time).total_seconds()
    
    if elapsed >= SCREENSHOT_COOLDOWN:
        # Cooldown sudah selesai
        return True
    
    print(f"[COOLDOWN] {icao}: {int(SCREENSHOT_COOLDOWN - elapsed)}s remaining")
    return False


def update_screenshot_time(icao):
    """
    Update waktu terakhir screenshot untuk sebuah pesawat
    """
    last_screenshot_time[icao] = datetime.now()


def get_aircraft_info(icao):
    """
    Dapatkan informasi aircraft dari history
    """
    if icao in aircraft_history:
        return {
            "history": aircraft_history[icao],
            "data_points": len(aircraft_history[icao]),
            "total_heading_change": calculate_heading_change(aircraft_history[icao])
        }
    return None


def clear_history(icao=None):
    """
    Clear history untuk aircraft tertentu, atau semua jika icao=None
    """
    global aircraft_history
    
    if icao:
        if icao in aircraft_history:
            del aircraft_history[icao]
    else:
        aircraft_history.clear()
