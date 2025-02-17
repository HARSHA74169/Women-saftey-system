import asyncio
import csv
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from bleak import BleakClient

# Fastrack Watch MAC Address
MAC_ADDRESS_FASTRACK = "FB:D8:57:5B:04:32"

# Characteristic UUIDs (from service scan)
HEART_RATE_UUID = "00002a37-0000-1000-8000-00805f9b34fb"  # Suspected HR
STEP_COUNT_UUID = "0000fee1-0000-1000-8000-00805f9b34fb"  # Suspected Steps


# Data storage for real-time graphing
time_data, heart_rate_data, step_count_data = [], [], []

# CSV File Setup
CSV_FILE = "/files/watch_data.csv"

# Initialize CSV File with Headers
with open(CSV_FILE, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Heart Rate", "Step Count"])


def extract_heart_rate(data):
    """Extracts heart rate from raw data (Assumption: First byte is HR)."""
    return data[0] if len(data) > 0 else None


def extract_step_count(data):
    """Extracts step count from raw data (Assumption: First 2 bytes are steps)."""
    return data[0] + (data[1] << 8) if len(data) > 1 else None


def notification_handler(sender, data):
    """ Debugging: Display raw and decoded data """
    int_values = list(data)  # Convert bytearray to list of integers
    hex_values = data.hex()  # Convert to hex for readability
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")

    print(f"\n[{timestamp}] Notification from {sender}:")
    print(f"  🔹 Raw Bytearray: {data}")
    print(f"  🔹 Hexadecimal: {hex_values}")
    print(f"  🔹 Integer Values: {int_values}")

    # Try extracting values
    if sender == HEART_RATE_UUID:
        heart_rate = extract_heart_rate(int_values)
        print(f"  ❤️ Extracted Heart Rate: {heart_rate} bpm")
    elif sender == STEP_COUNT_UUID:
        step_count = extract_step_count(int_values)
        print(f"  👣 Extracted Step Count: {step_count}")

    # Log only if values are found
    if heart_rate or step_count:
        with open(CSV_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, heart_rate or "", step_count or ""])

async def read_and_notify():
    """Connects to the smartwatch and enables notifications for heart rate and step count."""
    async with BleakClient(MAC_ADDRESS_FASTRACK) as client:
        if client.is_connected:
            print("✅ Connected to Fastrack smartwatch!")

            # Enable notifications
            await client.start_notify(HEART_RATE_UUID, notification_handler)
            await client.start_notify(STEP_COUNT_UUID, notification_handler)
            print("📡 Listening for Heart Rate and Step Count...")

            # Keep running to receive data
            await asyncio.sleep(60)  # Change to adjust runtime

            # Stop notifications
            await client.stop_notify(HEART_RATE_UUID)
            await client.stop_notify(STEP_COUNT_UUID)
            print("⏹ Stopped notifications.")


def update_graph(frame):
    """Updates the live graph with new data."""
    plt.clf()
    plt.title("Live Heart Rate & Step Count Data")
    plt.xlabel("Time")
    plt.ylabel("Values")
    plt.xticks(rotation=45)
    plt.grid(True)

    if heart_rate_data:
        plt.plot(time_data, heart_rate_data, label="Heart Rate (bpm)", color="red", marker="o")
    if step_count_data:
        plt.plot(time_data, step_count_data, label="Step Count", color="blue", marker="s")

    plt.legend()
    plt.tight_layout()


def start_live_graph():
    """Starts the real-time plotting of heart rate and step count."""
    ani = animation.FuncAnimation(plt.gcf(), update_graph, interval=2000)
    print("📊 Opening live graph...")
    plt.show()


if __name__ == "__main__":
    # Run BLE data collection asynchronously
    asyncio.run(read_and_notify())

    # Start live graph after collecting data
    start_live_graph()
