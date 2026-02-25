# FlightRadar24 API Configuration
API_KEY = "019c93f2-f71d-70c2-93cf-428aa10fe301|qA6RgSa5mAr7FQlP9i7Yo1c06zaYgRbTZRsEv80d7c441b43"

BASE_URL = "https://fr24api.flightradar24.com/api/live/flight-positions/light"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept-Version": "v1",
    "Accept": "application/json"
}

# ============================================
# LOKASI BANDAR UDARA INTERNASIONAL JUANDA (SUB)
# ============================================
# Koordinat: -7.3798° LS, 112.7868° BT
# Elevasi: 3 meter di atas permukaan laut

JUANDA_LAT = -7.379
JUANDA_LON = 112.787
JUANDA_ZOOM = 12  # Zoom level untuk melihat holding pattern

# ============================================
# BOUNDING BOX UNTUK AREA JUANDA
# ============================================
# Format: "south_lat,west_lon,north_lat,east_lon"
# Coverage: Seluruh Jawa Timur dan Laut Jawa

# BOUNDS_JUANDA_EXTENDED - Area luas (lebih banyak pesawat)
BOUNDS_JUANDA_EXTENDED = "-8.5,111.5,-6.5,114.5"

# BOUNDS_JUANDA_LOCAL - Area dekat bandara
BOUNDS_JUANDA_LOCAL = "-8,112,-7,113.5"

# Pilih bounding box yang ingin digunakan
BOUNDS = BOUNDS_JUANDA_LOCAL  # Default: area lokal Juanda

# ============================================
# PENGATURAN DETEKSI HOLDING PATTERN
# ============================================

# Interval cek flights dalam detik
CHECK_INTERVAL = 30  # Cek setiap 30 detik

# Minimum perubahan heading total (dalam derajat) untuk deteksi holding
# Nilai 300 berarti pesawat telah berputar minimal ~300° (hampir satu lingkaran penuh)
HOLDING_HEADING_THRESHOLD = 300

# Minimum jumlah data points untuk mulai mendeteksi
MIN_DATA_POINTS = 5

# Maksimal history points yang disimpan per pesawat
MAX_HISTORY_POINTS = 20

# ============================================
# PENGATURAN SCREENSHOT
# ============================================

# Cooldown antara screenshot (dalam detik)
# 900 detik = 15 menit
SCREENSHOT_COOLDOWN = 900

# Folder untuk menyimpan screenshot
SCREENSHOT_FOLDER = "logs"

# Format nama file screenshot
SCREENSHOT_PREFIX = "HOLDING"

# ============================================
# PENGATURAN BROWSER (PLAYWRIGHT)
# ============================================

# Chrome user data directory (gunakan profile yang sudah login)
CHROME_USER_DATA = r"C:\Users\alvin\AppData\Local\Google\Chrome\User Data\Profile 5"

# Viewport size untuk screenshot
VIEWPORT_WIDTH = 1920
VIEWPORT_HEIGHT = 1080

# Timeout untuk navigasi halaman (ms)
PAGE_TIMEOUT = 30000

# Timeout untuk klik element (ms)
CLICK_TIMEOUT = 5000
