# Women Safety Smartwatch System

A compact, wearable safety system designed to monitor biometric data in real-time and trigger emergency alerts. It connects via Bluetooth to compatible smartwatches to track vital metrics and detect potential distress patterns, aiming to enhance personal safety, particularly for women.

## 🌟 Features

* **Real-time Health Monitoring**: Tracks heart rate, step count, and battery status.
* **Emotion Detection**: Analyzes biometric data to classify emotional states.
* **Emergency Alert System**: Sends automatic SMS alerts via Twilio.
* **Watch Removal Detection**: Identifies unexpected device removal.
* **Bluetooth Device Discovery**: Scans and connects to BLE-supported smartwatches.
* **Location Tracking**: Includes GPS coordinates in alerts.
* **Historical Data**: Stores and displays past sensor readings.
* **Web Dashboard**: Centralized dashboard for real-time monitoring and device management.

## 🏗️ System Architecture

```
women-safety-system/
├── backend/                 # Flask API server
│   ├── app.py              # Main Flask application
│   └── app/
│       ├── alerts/         # SMS and emergency alert services
│       ├── routes/         # API endpoints
│       └── services/       # Core logic for sensor/emotion handling
├── frontend/               # React-based monitoring dashboard
│   └── src/
│       └── components/     # UI components
├── scripts/                # Bluetooth + sensor utilities
│   ├── watchdetails.py    # BLE smartwatch connector
│   ├── discover_devices.py # Bluetooth scanning tool
│   └── detectemotion.py   # Emotion classification
└── README.md
```

## 🚀 Quick Start

### Requirements

* Python 3.8+
* Node.js 16+
* Bluetooth-enabled device
* Twilio account
* BLE-compatible smartwatch

### Backend Setup

```bash
pip install flask flask-cors bleak twilio geocoder
cd backend
python app.py  # Runs at http://localhost:5000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev  # Runs at http://localhost:5173
```

### Connect Smartwatch

```bash
cd scripts
python discover_devices.py  # Find your watch
python watchdetails.py      # Connect and start reading
```

Update the `MAC_ADDRESS` in `watchdetails.py` accordingly.

## 📱 Supported Devices

* Mi Band series
* Honor Band
* Samsung Galaxy Watch
* Fitbit
* Generic BLE fitness trackers

BLE UUIDs:

* Heart Rate: `0000180d`
* Battery: `0000180f`
* Step Counter: Custom UUIDs

## 🔧 API Endpoints

| Endpoint               | Method | Description                  |
| ---------------------- | ------ | ---------------------------- |
| `/scan`                | GET    | Discover Bluetooth devices   |
| `/connect/<device_id>` | POST   | Connect to a smartwatch      |
| `/history`             | GET    | Fetch past sensor data       |
| `/api/alerts`          | GET    | View recent emergency alerts |
| `/check_health`        | POST   | Analyze sensor readings      |

## 🚨 Emergency Detection Logic

* **High HR**: >120 BPM → Stress signal
* **Low HR**: <60 BPM → Medical risk
* **Rapid Step Count**: Running or fleeing
* **Watch Removed**: Disconnected unexpectedly
* **Inactivity**: Long pause with high HR

### Alert Flow

1. Evaluate biometric data
2. Trigger SMS via Twilio
3. Attach GPS location
4. Log incident in SQLite database
5. Notify via frontend dashboard

## 🗃️ Database Schema (SQLite)

**sensor\_data**

```sql
CREATE TABLE sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    heart_rate INTEGER,
    step_count INTEGER,
    battery_level INTEGER,
    device_id TEXT,
    emotion TEXT
);
```

**alerts**

```sql
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    status TEXT NOT NULL
);
```

## 🧠 Emotion Classifier

* **Stressed**: HR > 120 BPM
* **Anxious**: HR > 90 + low activity
* **Energetic**: HR > 90 + high activity
* **Relaxed**: HR < 60 BPM
* **Neutral**: 60–90 BPM normal

## 🔐 Security Considerations

* **Encrypted Storage**: Protects biometric and alert logs
* **Location Sharing**: Only during alerts
* **Secure API Access**: Role-based endpoint control
* **Local-First Design**: Stores data on device unless opted otherwise

## ⚙️ Configuration

Modify thresholds in `backend/app/alerts/smsalert.py`:

```python
HR_THRESHOLD_HIGH = 140
HR_THRESHOLD_LOW = 50
STEP_THRESHOLD = 50
WATCH_TIMEOUT = 10  # seconds
```

Set your Twilio credentials:

```python
TWILIO_SID = "your_sid"
TWILIO_AUTH_TOKEN = "your_token"
TWILIO_PHONE = "+1234567890"
EMERGENCY_CONTACT = "+91XXXXXXXXXX"
```

## 🛠 Troubleshooting

* **Bluetooth Issues**: Ensure device is BLE-capable and MAC is correct
* **No Data**: Verify UUID support on your smartwatch
* **SMS Failures**: Check Twilio config and phone verification
* **Debugging**: Enable logging with `logging.DEBUG`

## 📈 Future Enhancements

* ML-based anomaly detection
* Native Android/iOS app
* Group monitoring for families
* Cloud backup options
* Geofencing & region alerts
* Voice-enabled SOS activation

---

**Note**: This system is intended to support personal safety but should be complemented with other safety practices.
