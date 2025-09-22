# post_to_servicenow.py
import network
import urequests
import time
from machine import ADC
import secrets  # 🔐 External file

adc = ADC(0)  # Moisture sensor analog pin

def read_moisture():
    value = adc.read()
    print("🌿 Moisture Reading:", value)
    return value

def connect_wifi():
    print("🔌 Connecting to Wi-Fi...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

    timeout = 10
    while not wlan.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1

    if wlan.isconnected():
        print("✅ Connected:", wlan.ifconfig())
    else:
        print("❌ Failed to connect to Wi-Fi")

def post_to_servicenow(moisture_level):
    url = f"{secrets.SN_INSTANCE}{secrets.SN_ENDPOINT}"
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "moisture_level": moisture_level,
        "source_device": "ESP8266",
        "note": "Live reading from ESP8266 sensor"
    }

    try:
        print(f"🌱 Posting moisture level {moisture_level} to ServiceNow...")
        response = urequests.post(
            url,
            json=payload,
            headers=headers,
            auth=(secrets.SN_USER, secrets.SN_PASSWORD)
        )
        print("📡 Response:", response.status_code)
        print(response.text)
        response.close()
    except Exception as e:
        print("❌ Error:", e)

# Run the program
connect_wifi()
if network.WLAN(network.STA_IF).isconnected():
    level = read_moisture()
    post_to_servicenow(level)
