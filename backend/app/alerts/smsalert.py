import time
import random  # Simulating smartwatch data
from twilio.rest import Client  # Twilio for SMS alerts
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.app.services.geolocation import get_device_location

import sqlite3
from datetime import datetime
# from backend.app.database import get_db, Alert  # Assuming you have a database module

# Twilio Credentials (replace with actual credentials)
TWILIO_SID = "AC196d87c333d0f55059efcbfceb8606fe"
TWILIO_AUTH_TOKEN = "892207d06a1b391a0e2de56621bca088"
TWILIO_PHONE = "+19207179504"
EMERGENCY_CONTACT = "+917416918937"

DB_NAME = "D:/women-safety-system/scripts/smartwatch_data.db"

# Function to send alert

# Database connection
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        status TEXT NOT NULL
    )
''')
conn.commit()

def send_alert(message):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    try:
        client.messages.create(
            body=message,
            from_=TWILIO_PHONE,
            to=EMERGENCY_CONTACT
        )
        status = "Sent"
    except Exception as e:
        print(f"Error sending alert: {e}")
        status = "Failed"

    # Store alert in the database
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO alerts (message, timestamp, status) VALUES (?, ?, ?)", (message, timestamp, status))
    conn.commit()

    print(f"ALERT SENT: {message}")
    
    
    # print(f"Location: {location_link}")
    
    # Store alert in the database
    # db = get_db()
    # new_alert = Alert(message=message, latitude=latitude, longitude=longitude)
    # db.add(new_alert)
    # db.commit()

# Threshold values
HR_THRESHOLD_HIGH = 140
HR_THRESHOLD_LOW = 50
SPO2_THRESHOLD = 90
STEP_THRESHOLD = 50  # Sudden increase
WATCH_TIMEOUT = 10  # Seconds without data = watch removed

# Simulated smartwatch data (Replace this with real sensor data)
def get_smartwatch_data():
    return {
        "heart_rate": random.randint(40, 180),  # Simulate HR
        "spo2": random.randint(85, 100),  # Simulate SpO2
        "steps": random.randint(0, 60),  # Simulate step count
        "watch_worn": random.choice([True, True, False]),  # Simulate watch removal
    }

# Monitoring function
def monitor_smartwatch():
    last_steps = 0
    last_watch_time = time.time()
    
    while True:
        data = get_smartwatch_data()
        print(f"Smartwatch Data: {data}")

        # Heart Rate check
        if data["heart_rate"] > HR_THRESHOLD_HIGH :
            send_alert(f"⚠️ High Heart Rate Detected! HR: {data['heart_rate']} BPM")

        if data["heart_rate"] < HR_THRESHOLD_LOW:
            send_alert(f"⚠️ Low Heart Rate Detected! HR: {data['heart_rate']} BPM")

        # SpO2 check
        if data["spo2"] < SPO2_THRESHOLD:
            send_alert(f"⚠️ Low Oxygen Level! SpO2: {data['spo2']}%")

        # Step Count check
        if data["steps"] - last_steps > STEP_THRESHOLD:
            send_alert(f"⚠️ Sudden running detected! Steps: {data['steps']}")

        last_steps = data["steps"]

        # Watch removal detection
        if not data["watch_worn"]:
            if time.time() - last_watch_time > WATCH_TIMEOUT:
                send_alert("⚠️ Watch removed! Possible danger.")
        else:
            last_watch_time = time.time()

        time.sleep(5)  # Simulate data collection every 5 seconds

# Run monitoring system
# monitor_smartwatch()
