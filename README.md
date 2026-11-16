# Migration Assessment Printer (Software Simulation)

A software-only Cloud Computing project prototype. It simulates the ESP32 and OLED in Python and provides a browser dashboard for assessing basic application CPU/RAM requirements, recommending a demo EC2 instance, and estimating monthly compute cost.

## 1. Requirements
- Python 3.10 or later
- VS Code (recommended)
- Internet browser

## 2. Run in VS Code terminal

Open this folder in VS Code, then run:

### Windows
```bash
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py app.py
```

Open http://127.0.0.1:5000

### macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 app.py
```

## 3. Device simulation
In another terminal:
```bash
py iot_simulator.py
```
This prints an MQTT-style sample request. It does not connect to AWS IoT Core.

## 4. Pricing modes
The default mode uses illustrative demo prices so the project runs without AWS credentials. The dashboard labels them as demo estimates, not live prices.

For live AWS Pricing API lookup:
1. Configure AWS credentials using an approved AWS account or lab role.
2. Ensure the identity has permission for `pricing:GetProducts`.
3. Set `USE_LIVE_PRICING=1` before starting the app.

Windows CMD:
```cmd
set USE_LIVE_PRICING=1
py app.py
```

PowerShell:
```powershell
$env:USE_LIVE_PRICING="1"
py app.py
```

The AWS Price List API client is created in `us-east-1`; the selected EC2 product region is passed as a pricing filter. Live results depend on AWS catalog availability and filters.

## 5. Important project scope
- `assessment.py`: classroom EC2 sizing logic.
- `pricing.py`: demo price mode and optional live AWS Pricing API integration.
- `iot_simulator.py`: local device/MQTT message simulation.
- `app.py`: Flask web application.
- `templates/index.html` and `static/style.css`: simulated OLED-style dashboard.

This is an educational prototype, not an official AWS migration recommendation. The monthly estimate uses 730 hours and excludes EBS storage, data transfer, taxes, support, snapshots, and other charges. The demo price table is illustrative and must not be presented as a current AWS quote.
