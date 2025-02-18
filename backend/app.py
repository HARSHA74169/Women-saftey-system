from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import asyncio
from bleak import BleakScanner
import logging
from typing import List, Optional


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

DB_NAME = "D:/women-safety-system/scripts/smartwatch_data.db"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SmartWatchScanner:
    def __init__(self, scan_time: float = 5.0):
        self.scan_time = scan_time
        self.devices = {}
        
    async def scan_for_watches(self) -> List[dict]:
        """Scan specifically for smartwatch devices"""
        try:
            # Common smartwatch service UUIDs
            WATCH_SERVICES = [
                "0000180d-0000-1000-8000-00805f9b34fb",  # Heart Rate Service
                "0000180f-0000-1000-8000-00805f9b34fb",  # Battery Service
                "0000181c-0000-1000-8000-00805f9b34fb",  # User Data Service
                "0000181e-0000-1000-8000-00805f9b34fb",  # Step Counter
            ]
            
            scanner = BleakScanner()
            devices = await scanner.discover(timeout=self.scan_time)
            
            watch_devices = []
            for device in devices:
                try:
                    # Check if device name contains common smartwatch keywords
                    if device.name and any(keyword in device.name.lower() 
                                         for keyword in ['watch', 'band', 'mi', 'honor', 'fitbit', 'galaxy']):
                        watch_devices.append({
                            "id": device.address,
                            "name": device.name or "Unknown Watch",
                            "rssi": device.rssi
                        })
                except Exception as e:
                    logger.error(f"Error processing device {device.address}: {str(e)}")
                    
            return watch_devices
            
        except Exception as e:
            logger.error(f"Error during scan: {str(e)}")
            return []

@app.route('/scan', methods=['GET'])
async def scan_devices():
    try:
        scanner = SmartWatchScanner()
        devices = await scanner.scan_for_watches()
        return jsonify(devices)
    except Exception as e:
        logger.error(f"Scan endpoint error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/connect/<device_id>', methods=['POST'])
async def connect_device(device_id):
    try:
        # Attempt to connect to the device
        async with BleakScanner() as scanner:
            device = await scanner.find_device_by_address(device_id)
            if not device:
                return jsonify({"error": "Device not found"}), 404
                
            return jsonify({"message": f"Successfully connected to {device.name}"})
    except Exception as e:
        logger.error(f"Connection error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Keep your existing history endpoint
@app.route('/history', methods=['GET'])
def get_sensor_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, heart_rate, step_count, battery_level, device_id, emotion FROM sensor_data ORDER BY timestamp DESC LIMIT 500")
    data = cursor.fetchall()
    conn.close()

    if data:
        return jsonify([{
            "timestamp": row[0],
            "heart_rate": row[1],
            "step_count": row[2],
            "battery_level": row[3],
            "device_id": row[4],
            "emotion" : row[5]
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

@app.route("/api/alerts", methods=["GET"])
def get_alerts():
    """Fetch recent alerts from SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, message, timestamp, status FROM alerts ORDER BY timestamp DESC LIMIT 10")
    
    alerts = cursor.fetchall()
    conn.close()
    
    if alerts:
        return jsonify([{
            "id": row[0], 
            "message": row[1], 
            "timestamp": row[2], 
            "status": row[3]
        } for row in alerts])
    
    return jsonify([])  # Return an empty array instead of 404


if __name__ == '__main__':
    app.run(debug=True, port=5000)