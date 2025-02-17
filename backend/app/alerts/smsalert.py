import time
import random  # Simulating smartwatch data
from twilio.rest import Client  # Twilio for SMS alerts

# Twilio Credentials (replace with actual credentials)
TWILIO_SID = "AC196d87c333d0f55059efcbfceb8606fe"
TWILIO_AUTH_TOKEN = "892207d06a1b391a0e2de56621bca088"
TWILIO_PHONE = "+19207179504"
EMERGENCY_CONTACT = "+917416918937"

# Function to send alert
def send_alert(message):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=TWILIO_PHONE,
        to=EMERGENCY_CONTACT
    )
    print(f"ALERT SENT: {message}")

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
monitor_smartwatch()
