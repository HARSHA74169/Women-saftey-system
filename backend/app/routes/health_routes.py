from flask import Blueprint, request, jsonify
from app.services.drastic_change import detect_drastic_change

health_routes = Blueprint('health_routes', __name__)

@health_routes.route('/check_health', methods=['POST'])
def check_health():
    """
    Endpoint to receive smartwatch data and detect drastic changes.
    Expected JSON format:
    {
        "heart_rate": 110,
        "steps": 4800,
        "spo2": 96
    }
    """
    data = request.json

    # Extract parameters
    current_heart_rate = data.get("heart_rate")
    current_steps = data.get("steps")
    current_spo2 = data.get("spo2")

    # Validate input
    if current_heart_rate is None or current_steps is None or current_spo2 is None:
        return jsonify({"error": "Missing health data"}), 400

    # Detect drastic changes
    result = detect_drastic_change(current_heart_rate, current_steps, current_spo2)

    return jsonify({"message": result})
