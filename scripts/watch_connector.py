import asyncio
from bleak import BleakClient, BleakScanner
import sqlite3

# Your smartwatch's service UUIDs (Replace these with actual values)
HEART_RATE_UUID = "00002a37-0000-1000-8000-00805f9b34fb"
STEP_COUNT_UUID = "00002a39-0000-1000-8000-00805f9b34fb"

async def find_watch():
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"Found device: {device.name}, Address: {device.address}")
    return devices

async def read_data(device_address):
    async with BleakClient(device_address) as client:
        if client.is_connected:
            print("Connected to watch!")

            # Read heart rate
            heart_rate = await client.read_gatt_char(HEART_RATE_UUID)
            heart_rate = int.from_bytes(heart_rate, byteorder="little")

            # Read step count
            step_count = await client.read_gatt_char(STEP_COUNT_UUID)
            step_count = int.from_bytes(step_count, byteorder="little")

            print(f"Heart Rate: {heart_rate}, Steps: {step_count}")

            # Store in SQLite
            store_data(heart_rate, step_count)

def store_data(heart_rate, step_count):
    conn = sqlite3.connect("sensor_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sensor_data (heart_rate, step_count) VALUES (?, ?)", (heart_rate, step_count))
    conn.commit()
    conn.close()

async def main():
    devices = await find_watch()
    if devices:
        device_address = devices[0].address  # Select the first found device
        while True:
            await read_data(device_address)
            await asyncio.sleep(1)  # Collect data every second

if __name__ == "__main__":
    asyncio.run(main())
