import time

# Thresholds for drastic changes
HR_THRESHOLD = 30  # Sudden change in heart rate (bpm)
STEP_THRESHOLD = 500  # Sudden drop in steps
SPO2_THRESHOLD = 5  # Sudden drop in SpO2 percentage
# Store previous values
previous_data = {"heart_rate": None, "steps": None, "spo2": None, "timestamp": None}

def detect_drastic_change(current_heart_rate, current_steps, current_spo2):
    """Detects drastic changes in heart rate, step count, and SpO2."""
    global previous_data
    alert_message = ""

    if previous_data["timestamp"]:
        time_diff = time.time() - previous_data["timestamp"]

        # Check drastic heart rate change
        if previous_data["heart_rate"] is not None:
            hr_diff = abs(current_heart_rate - previous_data["heart_rate"])
            if hr_diff >= HR_THRESHOLD:
                alert_message += f"⚠️ Drastic heart rate change detected: {hr_diff} bpm.\n"

        # Check drastic step count change
        if previous_data["steps"] is not None:
            step_diff = abs(current_steps - previous_data["steps"])
            if step_diff >= STEP_THRESHOLD:
                alert_message += f"⚠️ Sudden step count drop: {step_diff} steps.\n"

        # Check drastic SpO2 change
        if previous_data["spo2"] is not None:
            spo2_diff = abs(current_spo2 - previous_data["spo2"])
            if spo2_diff >= SPO2_THRESHOLD:
                alert_message += f"⚠️ Sudden SpO2 drop: {spo2_diff}%.\n"

    # Update previous data
    previous_data = {
        "heart_rate": current_heart_rate,
        "steps": current_steps,
        "spo2": current_spo2,
        "timestamp": time.time()
    }

    return alert_message if alert_message else "✅ No drastic changes detected."
