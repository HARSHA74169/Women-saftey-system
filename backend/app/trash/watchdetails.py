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
from datetime import datetime
import pytz
import os
import sys

from backend.app.services.geolocation import get_device_location
# sys.path.append(os.path.abspath(os.path.join('..')))

from backend.app.alerts.smsalert import send_alert

IST = pytz.timezone('Asia/Kolkata')



from backend.app.alerts.smsalert import send_alert

IST = pytz.timezone('Asia/Kolkata')

WATCH_REMOVAL_THRESHOLD = 10 

class SmartWatchServices(Enum):
    """List of smartwatch services"""
    GENERIC_ACCESS = "00001800-0000-1000-8000-00805f9b34fb"
    BATTERY = "0000180f-0000-1000-8000-00805f9b34fb"
    HEART_RATE = "0000180d-0000-1000-8000-00805f9b34fb"
    DEVICE_INFO = "0000180a-0000-1000-8000-00805f9b34fb"
    ACTIVITY_SERVICE = "0000feea-0000-1000-8000-00805f9b34fb"

class SmartWatchCharacteristics(Enum):
    """List of smartwatch characteristics"""
    BATTERY_LEVEL = "00002a19-0000-1000-8000-00805f9b34fb"
    HEART_RATE_MEASUREMENT = "00002a37-0000-1000-8000-00805f9b34fb"
    STEP_COUNT_UUID = "0000fee1-0000-1000-8000-00805f9b34fb"

class SmartWatchReader:
    def __init__(self, address):
        self.address = address
        self.client = None
        self.last_step_count = None
        self.db_connection = sqlite3.connect("smartwatch_data.db")
        self.db_cursor = self.db_connection.cursor()
        self.setup_database()

    def setup_database(self):
        """Initialize the database tables."""
        self.db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                heart_rate INTEGER,
                step_count INTEGER,
                battery_level INTEGER,
                device_id TEXT,
                UNIQUE(timestamp, heart_rate, step_count, battery_level, device_id)
            )
        """)
        self.db_connection.commit()

    async def connect(self):
        """Connect to the smartwatch"""
        try:
            self.client = BleakClient(self.address)
            await self.client.connect()
            print(f"Connected: {self.client.is_connected}")
            return True
        except Exception as e:
            print(f"Connection error: {str(e)}")
            return False

    async def read_battery(self):
        """Read battery level"""
        try:
            battery_level = await self.client.read_gatt_char(SmartWatchCharacteristics.BATTERY_LEVEL.value)
            self.last_battery_level = int(battery_level[0])
            return self.last_battery_level
        except Exception as e:
            print(f"Error reading battery: {str(e)}")
            return None

    def insert_sensor_data(self, heart_rate, step_count, battery_level):
        """Insert heart rate, step count, and battery level into SQLite without redundancy."""
        try:
            timestamp = datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S')
            self.db_cursor.execute("""
                INSERT OR IGNORE INTO sensor_data (timestamp, heart_rate, step_count, battery_level, device_id)
                VALUES (?, ?, ?, ?, ?)
            """, (timestamp, heart_rate, step_count, battery_level, self.address))
            self.db_connection.commit()
        except sqlite3.Error as e:
            print(f"Database error: {str(e)}")

    def heart_rate_handler(self, sender, data):
        """Handle heart rate notifications"""
        heart_rate = data[1] if len(data) > 1 else data[0]
        step_count = self.last_step_count if self.last_step_count is not None else 0
        battery_level = self.last_battery_level if hasattr(self, 'last_battery_level') else None
        print(f"Heart Rate: {heart_rate} BPM | Step Count: {step_count} | Battery Level: {battery_level}%")
        self.insert_sensor_data(heart_rate, step_count, battery_level)

    def step_count_handler(self, sender, data):
        """Handle step count notifications"""
        self.last_step_count = struct.unpack("<H", data[:2])[0]
        print(f"Step Count: {self.last_step_count}")

    async def check_watch_removal(self):
        """Background task to detect if the watch is removed."""
        while True:
            elapsed_time = (datetime.now() - self.last_heart_rate_time).total_seconds()
            if elapsed_time > WATCH_REMOVAL_THRESHOLD and not self.watch_removed:
                self.watch_removed = True
                print(f"⚠️ Watch removed! No heart rate detected for {WATCH_REMOVAL_THRESHOLD} seconds.")
                
                message = f"⚠️ Watch removed! No heart rate detected for {WATCH_REMOVAL_THRESHOLD} seconds."
                geo_location = get_device_location()
                latitude, longitude = geo_location['latitude'], geo_location['longitude']
                location_link = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"
                message += (str)(location_link)
                send_alert(message)
                
            await asyncio.sleep(1)

    async def start_monitoring(self):
        """Start monitoring heart rate and step count"""
        try:
            await self.client.start_notify(SmartWatchCharacteristics.HEART_RATE_MEASUREMENT.value, self.heart_rate_handler)
            await self.client.start_notify(SmartWatchCharacteristics.STEP_COUNT_UUID.value, self.step_count_handler)
            print("Monitoring heart rate, step count, and battery level...")
        except Exception as e:
            print(f"Error starting monitoring: {str(e)}")
            
        asyncio.create_task(self.check_watch_removal())
        

    async def disconnect(self):
        """Disconnect from the device"""
        if self.client and self.client.is_connected:
            await self.client.disconnect()
            print("Disconnected")
        self.db_connection.close()

async def main():
    """Main function to connect and retrieve smartwatch data"""
    MAC_ADDRESS = "FB:D8:57:5B:04:32"  # Updated MAC address
    watch = SmartWatchReader(MAC_ADDRESS)
    
    try:
        if await watch.connect():
            battery = await watch.read_battery()
            if battery is not None:
                print(f"Battery Level: {battery}%")

            await watch.start_monitoring()

            print("\nMonitoring continuously. Press Ctrl+C to stop.")
            while True:
                await asyncio.sleep(1)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        await watch.disconnect()

if __name__ == "__main__":
    asyncio.run(main())