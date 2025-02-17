import sqlite3
import time
from datetime import datetime, timedelta

def get_last_30_seconds_data():
    """Retrieve sensor data from the last 30 seconds"""
    conn = sqlite3.connect('smartwatch_data.db')
    cursor = conn.cursor()
    
    time_threshold = datetime.now() - timedelta(seconds=30)
    cursor.execute("""
        SELECT timestamp, heart_rate, step_count FROM sensor_data
        WHERE timestamp >= ? ORDER BY timestamp DESC
    """, (time_threshold.strftime('%Y-%m-%d %H:%M:%S'),))
    
    data = cursor.fetchall()
    conn.close()
    return data

def classify_emotion(heart_rate):
    """Classify emotion based on heart rate"""
    if heart_rate < 60:
        return "Calm/Relaxed"
    elif 60 <= heart_rate <= 100:
        return "Normal"
    elif 100 < heart_rate <= 130:
        return "Excited/Active"
    else:
        return "Anxious/Stressed"

def detect_running(step_data):
    """Detect if the user is running based on step count changes"""
    if len(step_data) < 2:
        return "Insufficient Data"
    
    latest_step = step_data[0]
    earliest_step = step_data[-1]
    
    step_difference = latest_step - earliest_step
    if step_difference > 10:
        return "Running"
    return "Not Running"

def analyze_data():
    """Analyze the last 30 seconds of smartwatch data"""
    data = get_last_30_seconds_data()
    
    if not data:
        print("No recent data available.")
        return
    
    heart_rates = [row[1] for row in data if row[1] is not None]
    step_counts = [row[2] for row in data if row[2] is not None]
    
    if heart_rates:
        avg_heart_rate = sum(heart_rates) / len(heart_rates)
        emotion = classify_emotion(avg_heart_rate)
        print(f"Average Heart Rate: {avg_heart_rate:.2f} BPM | Emotion: {emotion}")
    
    if step_counts:
        running_state = detect_running(step_counts)
        print(f"Running State: {running_state}")

if __name__ == "__main__":
    while True:
        analyze_data()
        time.sleep(5)  # Run analysis every 5 seconds
