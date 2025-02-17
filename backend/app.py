from flask import Flask, jsonify
import sqlite3
from flask_cors import CORS
import os   

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




if __name__ == '__main__':
    app.run(debug=True, port=5000)
