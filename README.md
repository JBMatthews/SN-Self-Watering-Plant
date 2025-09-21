# 🌿 Self-Watering System — Version 1

**v1 Summary:**  
A Raspberry Pi reads soil moisture levels and sends the data to ServiceNow. If the soil status is `dry`, ServiceNow sends a mobile notification prompting the user to water the plant manually.

---

## 🧠 Overview

This project bridges IoT and enterprise automation by combining a Raspberry Pi moisture sensor with a ServiceNow-based workflow system. The current version lays the groundwork for full automation by enabling real-time logging and alerting when your plant is too dry.

---

## 🔁 System Workflow

1. **Moisture Sensor → Pi:**  
   The Raspberry Pi reads the soil moisture value using a digital or analog sensor.

2. **Pi → ServiceNow:**  
   The Pi sends a POST request to a Scripted REST API in ServiceNow with:
   - `moisture_level`
   - `status` (`dry`, `ok`, or `watered`)
   - `source_device`

3. **ServiceNow → Log Table:**  
   Data is stored in the `Log` table with key fields:
   - `moisture_level` (decimal)
   - `status` (choice field)
   - `was_watered` (boolean)
   - `note`
   - `severity` (info/warning/critical)

4. **Log → Flow:**  
   A Flow Designer workflow listens for new log entries.  
   If `status = dry`, it sends a **mobile notification** (email or push) to alert the user.

---

## 🧱 Key Components

### ✅ Raspberry Pi
- Python script reads moisture (currently simulated)
- Sends HTTP POST to ServiceNow
- Uses virtual environment + `requests` library

### ✅ ServiceNow
- Scoped App: `Self-Watering System`
- Tables:
  - `Log` – stores sensor data
- Scripted REST API:
  - Endpoint: `/api/x_yourscope/self_water_api/log`
- Flow:
  - Trigger: new Log with `status = dry`
  - Action: send mobile/email alert

---

## 🧪 Testing

### Manual Log Insert:
To simulate a dry event in ServiceNow:

- Go to `Self-Watering System > Log > New`
- Set:
  - `moisture_level` = `15.0`
  - `status` = `dry`
- Save the record
- You should receive a notification

zx### Pi-side Test:
Run `moisture_sensor_code.py` and verify:
- Successful POST (HTTP 201)
- New Log entry appears in SN
- Alert triggers if `status = dry`

---

## 🔜 Coming in Version 2

- Config table to manage moisture thresholds, watering duration, and auto-watering flag
- Webhook or polling from Pi for SN-initiated watering
- Dashboard to visualize trends
- Multi-device support

---

## 📅 Status

- ✅ Version 1 complete and tested
- 🧪 Ready for sensor integration
- 🔁 Live sync with GitHub repo

---

Created by James Matthews  
MIT License
