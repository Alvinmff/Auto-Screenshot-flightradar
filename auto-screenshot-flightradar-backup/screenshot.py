from playwright.sync_api import sync_playwright
from datetime import datetime
import os

def take_screenshot(callsign):
    """
    Take a screenshot of the flight on FlightRadar24
    Focuses on the aircraft around Juanda airport area
    """
    
    # URL dengan koordinat sekitar Juanda: -7.379, 112.787
    # Format: https://www.flightradar24.com/{callsign}/{lat},{lon}/{zoom_level}
    # Zoom level 12 memberikan视野 yang baik untuk melihat holding pattern
    lat = -7.379
    lon = 112.787
    zoom = 12
    
    url = f"https://www.flightradar24.com/{callsign}/{lat},{lon}/{zoom}"
    
    print(f"[SCREENSHOT] Opening {url}")
    
    # Buat folder logs jika belum ada
    os.makedirs("logs", exist_ok=True)
    
    # Generate filename dengan timestamp dan callsign
    filename = f"logs/HOLDING_{callsign}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    
    # Chrome user data directory (persistent session)
    chrome_user_data = r"C:\Users\alvin\AppData\Local\Google\Chrome\User Data\Profile 5"

    with sync_playwright() as p:
        # Launch persistent Chrome context
        context = p.chromium.launch_persistent_context(
            user_data_dir=chrome_user_data,
            channel="chrome",
            headless=False,
            viewport={"width": 1920, "height": 1080}
        )

        page = context.new_page()

        # Navigate to the flight URL
        page.goto(url, wait_until="networkidle", timeout=30000)
        
        # Klik tombol Agree pada cookie popup jika muncul
        try:
            page.get_by_text("Agree and close", exact=True).click(timeout=5000)
            print("[INFO] Cookie popup closed")
        except Exception:
            # Jika popup tidak muncul, lanjutkan saja
            print("[INFO] No cookie popup found")
        
        # Tunggu halaman load completely
        page.wait_for_timeout(5000)
        
        # Zoom out sedikit untuk melihat pattern holding lebih jelas
        # Tekan minus key beberapa kali untuk zoom out
        for _ in range(2):
            page.keyboard.press("Minus")
            page.wait_for_timeout(500)

        # Tunggu sebentar untuk render complete
        page.wait_for_timeout(2000)

        # Ambil screenshot
        page.screenshot(path=filename, full_page=True)
        print(f"[SCREENSHOT SAVED] {filename}")

        # Tutup context
        context.close()
        
    return filename


if __name__ == "__main__":
    # Test langsung dengan callsign contoh
    test_callsign = "GIA927"
    print(f"Testing screenshot function with {test_callsign}...")
    take_screenshot(test_callsign)
