import machine
import time
import urequests
import connect
from secrets import secrets

connect.connect()

adc = machine.ADC(0)
relay = machine.Pin(14, machine.Pin.OUT)

SN_INSTANCE = secrets['instance']
SN_API_PATH = "/api/x_461782_slf_water/self_watering_api/log"
USERNAME = secrets['username']
PASSWORD = secrets['password_sn']

def log_to_servicenow(percent, status):
    payload = {
        "moisture_level": percent,
        "status": status,
        "source_device": "esp8266-v2"
    }
    try:
        url = f"https://{SN_INSTANCE}{SN_API_PATH}"
        res = urequests.post(url, json=payload, auth=(USERNAME, PASSWORD))
        print("✅ Sent to SN:", payload, "| Response:", res.status_code)
        res.close()
    except Exception as e:
        print("❌ SN POST error:", e)

while True:
    raw = adc.read()
    percent = 100 - int((raw / 1023) * 100)

    if percent > 70:
        status = "watered"
    elif percent < 40:
        status = "dry"
    else:
        status = "ok"

    print(f"🌱 Moisture: {percent}% | Status: {status}")
    log_to_servicenow(percent, status)

    if status == "dry":
        print("🚿 Watering plant...")
        relay.value(1)
        time.sleep(3)
        relay.value(0)

    print("⏳ Sleeping for 10 minutes...\n")
    time.sleep(200)
