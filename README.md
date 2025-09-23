# Self-Watering Plant System

Welcome to the **Self-Watering Plant Project Hub**! This system combines hardware automation, microcontroller programming, and ServiceNow integration to create a smart, self-watering solution that can scale from a single potted plant to an entire window garden of microgreens.

---

## Project Overview

This project uses a **capacitive soil moisture sensor**, a **relay-controlled water pump**, and an **ESP8266 microcontroller** running MicroPython to:

- Automatically detect soil moisture levels
- Trigger a pump to water the plant
- Send moisture + watering data to ServiceNow
- Allow remote viewing/control via a ServiceNow dashboard

---

## Architecture

```plaintext
┌───────────────────┐        WiFi         ┌────────────────────────────┐
│ ESP8266 (MicroPy) │ ──────────────────▶ │ ServiceNow (PDI Instance)  │
│ └─ moisture sensor│                     │ └─ x_461782_slf_water_log  │
│ └─ water pump     │                     │ └─ x_461782_slf_water_sys  │
└───────────────────┘                     └────────────────────────────┘
```

---

## Hardware Components

| Component            | Model / Specs                             |
|----------------------|--------------------------------------------|
| Microcontroller      | ESP8266 (HiLetGo Dev Board)                |
| Moisture Sensor      | Capacitive Soil Sensor (Analog Output)     |
| Relay Module         | 4-Channel Relay Board (Active Low Trigger) |
| Submersible Pump     | 3–5V DC Micro Pump                          |
| Tubing               | 5/32" or 4mm ID silicone tubing             |
| Power                | USB Adapter (5V/2A)                         |
| Wiring               | Male-to-Female jumper wires, terminals     |

---

## Folder Structure

```plaintext
self-watering-system/
├── README.md
├── sn_source_control.properties                  # Studio Source Control linking metadata
│
├── b5c99759531de210130451a0a0490e26/            # ServiceNow app XML (scoped app updates)
│   ├── README.md
│   ├── checksum.txt
│   ├── dictionary/                              # Table definitions (log, settings, etc.)
│   ├── update/                                  # Update records (UI Action, Flow, API op, etc.)
│   └── author_elective_update/                  # Choices, UI policy, etc.
│
├── servicenow/
│   ├── api_docs.md                              # REST endpoint docs for devices
│   └── post_moisture_data.js                    # Simple example sender (local test)
│
├── hardware/
│   ├── esp8266/
│   ├── main.py                              # Production loop (reads % moisture, waters, logs to SN)
│   ├── secrets.py                           # Wi-Fi & SN creds + thresholds (gitignored)
│   ├── pump_test.py                         # Quick relay/pump test (GPIO only)
│   └── webrepl/                             # WebREPL client & helpers
│      ├── webrepl_cli.py
│      ├── webrepl.html
│      ├── webrepl.js
│      ├── webrepl.css
│      ├── term.js
│      ├── FileSaver.js
│      └── README.md
│   
```

---

## How It Works

1. `main.py` runs a loop every 5 minutes.
2. Reads raw moisture level and converts to % (0–100).
3. If below threshold (e.g., 35%), it waters for a few seconds.
4. Sends logs (moisture + watered) to ServiceNow via REST API.
5. You can view this in SN or manually trigger emergency watering.

---

## Useful Thonny / CLI Commands

| Action                            | Command or Instruction |
|----------------------------------|-------------------------|
| Upload to ESP (WebREPL)          | `webrepl_cli.py -p waterme filename.py 10.0.0.105:` |
| Run `main.py` via Thonny         | F5 (with interpreter set to MicroPython ESP8266) |
| Soft reboot ESP                  | `Ctrl+D` or type `import machine; machine.reset()` |
| Test pump manually               | `pump_test.py` |
| View serial output               | Thonny REPL |
| Install WebREPL CLI dependencies| `pip install websocket-client` |
| Activate virtualenv (Mac)       | `source .venv/bin/activate` |

---

## Secrets & Configs

Provided is a sample of what should be in `secrets.py`:

```python
SSID = "wifi_name"
PASSWORD = "wifi_password"
INSTANCE = "sn_pdi_url.service-now.com"
USER = "admin"
USER_PASSWORD = "pdi_password"
ENDPOINT = "/api/end_point/path"
RELAY_PIN = (pin used by ESP - mine uses "14")
```
**Don't commit secrets.py to GitHub!** (Already in `.gitignore`)

---

## Roadmap

| Phase | Description |
|-------|-------------|
| Phase 1 | Single-plant watering + SN logging |
| Phase 2 | Multi-plant support (scale to 4 pumps) |
| Phase 3 | Window Garden w/ dashboard + remote controls |
| Future | ESP32 upgrade, OTA updates, SN mobile integration |

---

## Debug Tips

- Use `print()` in `main.py` to debug values and logic.
- Confirm `relay.value(1)` activates pump (test script).
- If device doesn’t connect: double-check `SSID` + `PASSWORD`.

---

## Built With

- [MicroPython](https://micropython.org/)
- [ESP8266](https://www.espressif.com/en/products/socs/esp8266)
- [ServiceNow App Engine](https://developer.servicenow.com/)
- [REST APIs](https://developer.servicenow.com/dev.do#!/reference/api)

---

## Author

**James B. Matthews**  
Atlanta, GA  
[GitHub](https://github.com/jamesbmatthews)  
[Website](https://jamesbmatthews.tech/)
