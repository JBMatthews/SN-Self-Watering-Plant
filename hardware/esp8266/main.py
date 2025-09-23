import network
import urequests
import machine
import time
import secrets  # Externalized config

# 🧠 Connect to Wi-Fi
def connect_wifi():
    print("🔌 Connecting to Wi-Fi...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
    while not wlan.isconnected():
        time.sleep(1)
    print("✅ Connected:", wlan.ifconfig())

# 🌡️ Read and convert analog moisture level to 0–100%
def read_moisture():
    analog_val = machine.ADC(0).read()  # ESP8266 A0 pin
    percent = 100 - int((analog_val / 1023) * 100)
    print(f"🌿 Moisture Level: {percent}% (raw: {analog_val})")
    return percent

# 🚰 Activate the relay to water the plant
def water():
    print(f"💧 Moisture below {secrets.MOISTURE_THRESHOLD}%, watering...")
    relay = machine.Pin(secrets.RELAY_PIN, machine.Pin.OUT)
    relay.on()
    time.sleep(secrets.WATERING_DURATION)
    relay.off()
    print("✅ Watering complete.")

# ☁️ Send data to ServiceNow
def send_to_servicenow(moisture_level):
    url = secrets.SERVICENOW_INSTANCE + secrets.SERVICENOW_ENDPOINT
    payload = {
        "moisture_level": moisture_level,
        "note": "Auto-sent from ESP8266",
        "source_device": "esp8266"
    }
    try:
        print(f"📡 Sending data to ServiceNow: {url}")
        response = urequests.post(
            url,
            json=payload,
            auth=(secrets.SERVICENOW_USER, secrets.SERVICENOW_PASS),
            headers={"Content-Type": "application/json"}
        )
        print("✅ Sent! Status:", response.status_code)
        print(response.text)
        response.close()
    except Exception as e:
        print("❌ Failed to send to ServiceNow:", e)

# 🪄 MAIN LOOP
def run():
    connect_wifi()
    while True:
        moisture = read_moisture()
        if moisture < secrets.MOISTURE_THRESHOLD:
            water()
        send_to_servicenow(moisture)
        print(f"⏱️ Sleeping for {secrets.SLEEP_DURATION}s...\n")
        time.sleep(secrets.SLEEP_DURATION)

run()
