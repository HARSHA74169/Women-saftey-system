from flask import Flask, jsonify
import sqlite3
from flask_cors import CORS
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import asyncio
from bleak import BleakScanner

from scripts.watchdetails import *
import asyncio  

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for frontend

DB_NAME = "D:/women-safety-system/scripts/smartwatch_data.db"

# Fetch latest heart rate & step count
@app.route('/sensordata', methods=['GET'])
def get_sensor_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, heart_rate, step_count, id FROM sensor_data ORDER BY timestamp DESC LIMIT 10")
    data = cursor.fetchall()
    conn.close()

    if data:
        return jsonify([{
            "timestamp": row[0],
            "heart_rate": row[1],
            "step_count": row[2],
            "id": row[3]
        } for row in data])
    return jsonify({"message": "No data found"}), 404
async def scan_ble_devices():
    devices = {}

    def device_found_callback(device, advertisement_data):
        devices[device.address] = {
            "name": device.name or "Unknown",
            "address": device.address,
            "rssi": advertisement_data.rssi,
        }

    scanner = BleakScanner(detection_callback=device_found_callback)
    await scanner.start()
    await asyncio.sleep(5)
    await scanner.stop()

    return list(devices.values())
@app.route('/scan', methods=['GET'])
def scan():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        devices = loop.run_until_complete(scan_ble_devices())

        return jsonify({"devices": devices, "count": len(devices)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
