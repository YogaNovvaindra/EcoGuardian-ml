from flask import Blueprint, jsonify, request
from exponen.co2 import get_forecast_co2

bp = Blueprint('main', __name__)

@bp.route('/forecast_co2', methods=['GET'])
def forecast_co2():
    # Get the 'esp_id' parameter from the query string
    esp_id = request.args.get('esp_id')

    if esp_id is None:
        return jsonify({"error": "Missing 'esp_id' parameter"}), 400

    # Use the 'esp_id' in your get_forecast_co2 function
    forecast_co2 = get_forecast_co2(esp_id)
    return jsonify({"Triple Exponential Smoothing Forecast": forecast_co2})
