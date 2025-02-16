from flask import Flask, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

DB_NAME = "sensor_data.db"

# Fetch latest heart rate & step count
@app.route('/api/sensor_data', methods=['GET'])
def get_sensor_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, heart_rate, step_count FROM sensor_data ORDER BY timestamp DESC LIMIT 1")
    data = cursor.fetchone()
    conn.close()

    if data:
        return jsonify({
            "timestamp": data[0],
            "heart_rate": data[1],
            "step_count": data[2]
        })
    return jsonify({"message": "No data found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
