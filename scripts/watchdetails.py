import asyncio
import sqlite3
from bleak import BleakClient
from enum import Enum
import struct
from datetime import datetime

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
        self.conn = sqlite3.connect('smartwatch_data.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sensor_data (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                                heart_rate INTEGER,
                                spo2 INTEGER,
                                step_count INTEGER,
                                battery_level INTEGER,
                                device_id TEXT)''')
        self.conn.commit()

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
            return int(battery_level[0])
        except Exception as e:
            print(f"Error reading battery: {str(e)}")
            return None

    def heart_rate_handler(self, sender, data):
        """Handle heart rate notifications"""
        heart_rate = data[1] if len(data) > 1 else data[0]
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Heart Rate: {heart_rate} BPM", end=" | ")
        if self.last_step_count is not None:
            print(f"Step Count: {self.last_step_count}")
            self.cursor.execute('''INSERT INTO sensor_data (timestamp, heart_rate, step_count, device_id) 
                                   VALUES (?, ?, ?, ?)''', (timestamp, heart_rate+60, self.last_step_count, self.address))
        else:
            print()
            self.cursor.execute('''INSERT INTO sensor_data (timestamp, heart_rate, device_id) 
                                   VALUES (?, ?, ?)''', (timestamp, heart_rate, self.address))
        self.conn.commit()

    def step_count_handler(self, sender, data):
        """Handle step count notifications"""
        self.last_step_count = struct.unpack("<H", data[:2])[0]
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Step Count: {self.last_step_count}")
        self.cursor.execute('''INSERT INTO sensor_data (timestamp, step_count, device_id) 
                               VALUES (?, ?, ?)''', (timestamp, self.last_step_count, self.address))
        self.conn.commit()

    async def start_monitoring(self):
        """Start monitoring heart rate and step count"""
        try:
            await self.client.start_notify(SmartWatchCharacteristics.HEART_RATE_MEASUREMENT.value, self.heart_rate_handler)
            await self.client.start_notify(SmartWatchCharacteristics.STEP_COUNT_UUID.value, self.step_count_handler)
            print("Monitoring heart rate and step count...")
        except Exception as e:
            print(f"Error starting monitoring: {str(e)}")

    async def disconnect(self):
        """Disconnect from the device"""
        if self.client and self.client.is_connected:
            await self.client.disconnect()
            print("Disconnected")
        self.conn.close()

async def main():
    """Main function to connect and retrieve smartwatch data"""
    MAC_ADDRESS = "FB:D8:57:5B:04:32"  # Updated MAC address
    
    watch = SmartWatchReader(MAC_ADDRESS)
    
    try:
        if await watch.connect():
            battery = await watch.read_battery()
            if battery is not None:
                print(f"Battery Level: {battery}%")
                watch.cursor.execute('''INSERT INTO sensor_data (battery_level, device_id) 
                                        VALUES (?, ?)''', (battery, MAC_ADDRESS))
                watch.conn.commit()

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
