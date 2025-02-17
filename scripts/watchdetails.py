import asyncio
import sqlite3
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bleak import BleakClient
from enum import Enum
import struct
from datetime import datetime
from bleak.backends.device import BLEDevice
from backend.app.alerts.smsalert import send_alert

# Constants
MAC_ADDRESS = "FB:D8:57:5B:04:32"
WATCH_REMOVAL_THRESHOLD = 5  # Seconds of continuous 0 heart rate

class SmartWatchServices(Enum):
    """Smartwatch services UUIDs"""
    HEART_RATE = "0000180d-0000-1000-8000-00805f9b34fb"

class SmartWatchCharacteristics(Enum):
    """Smartwatch characteristics UUIDs"""
    HEART_RATE_MEASUREMENT = "00002a37-0000-1000-8000-00805f9b34fb"
    STEP_COUNT_UUID = "0000fee1-0000-1000-8000-00805f9b34fb"

class SmartWatchReader:
    def __init__(self, address):
        self.address = address
        self.client = None
        self.last_step_count = None
        self.watch_removed = False
        self.last_heart_rate_time = datetime.now()

        # Initialize database
        self.conn = sqlite3.connect('smartwatch_data.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sensor_data (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                                heart_rate INTEGER,
                                step_count INTEGER,
                                device_id TEXT)''')
        self.conn.commit()

    async def connect(self):
        """Connect to the smartwatch."""
        try:
            self.client = BleakClient(self.address)
            await self.client.connect()
            return self.client.is_connected
        except Exception as e:
            print(f"Connection error: {str(e)}")
            return False

    def heart_rate_handler(self, sender, data):
        """Handle heart rate notifications and detect watch removal."""
        heart_rate = data[1] if len(data) > 1 else data[0]
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if heart_rate == 0:
            return  # Don't store continuous 0 heart rate, handled in background check

        # Reset watch removal flag when heart rate resumes
        if self.watch_removed:
            print("Watch reconnected! Heart rate detected again.")
            self.watch_removed = False

        self.last_heart_rate_time = datetime.now()
        
        print(f"Heart Rate: {heart_rate} BPM")
        
        # Store heart rate in database
        with self.conn:
            self.cursor.execute('''INSERT INTO sensor_data (timestamp, heart_rate, step_count, device_id) 
                                   VALUES (?, ?, ?, ?)''', 
                                (timestamp, heart_rate, self.last_step_count, self.address))

    async def check_watch_removal(self):
        """Background task to detect if the watch is removed."""
        while True:
            elapsed_time = (datetime.now() - self.last_heart_rate_time).total_seconds()
            if elapsed_time > WATCH_REMOVAL_THRESHOLD and not self.watch_removed:
                self.watch_removed = True
                print("⚠️ Watch removed! No heart rate detected for 5 seconds.")
                send_alert("⚠️ Watch removed! Possible danger.")
            await asyncio.sleep(1)

    async def start_monitoring(self):
        """Start monitoring heart rate and step count."""
        try:
            await self.client.start_notify(SmartWatchCharacteristics.HEART_RATE_MEASUREMENT.value, self.heart_rate_handler)
            print("Monitoring heart rate...")

            # Start background task for watch removal detection
            asyncio.create_task(self.check_watch_removal())

        except Exception as e:
            print(f"Error starting monitoring: {str(e)}")

    async def disconnect(self):
        """Disconnect from the device."""
        if self.client and self.client.is_connected:
            await self.client.disconnect()
            print("Disconnected from smartwatch.")
        self.conn.close()

async def main():
    """Main function to connect and retrieve smartwatch data."""
    watch = SmartWatchReader(MAC_ADDRESS)

    try:
        if await watch.connect():
            await watch.start_monitoring()

            # Keep running until manually stopped
            while True:
                await asyncio.sleep(1)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        await watch.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
