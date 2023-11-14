from flask import Blueprint, jsonify, request
from exponen.co2 import get_forecast_co2
from exponen.humidity import get_forecast_humidity
from exponen.mq2 import get_forecast_mq2
from exponen.temperature import get_forecast_temperature
from exponen.pm25 import get_forecast_pm25
from exponen.uji import triple_exponential_smoothing
from ispu.ispu_co2 import get_ispu_co2
from ispu.ispu_pm25 import get_ispu_pm25
from ispu.ispu_co import get_ispu_co
from output.display import get_display
from output.mean import get_mean


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

@bp.route('/forecast_humidity', methods=['GET'])
def forecast_humidity():
    # Get the 'esp_id' parameter from the query string
    esp_id = request.args.get('esp_id')

    if esp_id is None:
        return jsonify({"error": "Missing 'esp_id' parameter"}), 400

    # Use the 'esp_id' in your get_forecast_humidity function
    forecast_humidity = get_forecast_humidity(esp_id)
    return jsonify({"Triple Exponential Smoothing Forecast": forecast_humidity})

@bp.route('/forecast_mq2', methods=['GET'])
def forecast_mq2():
    # Get the 'esp_id' parameter from the query string
    esp_id = request.args.get('esp_id')

    if esp_id is None:
        return jsonify({"error": "Missing 'esp_id' parameter"}), 400

    # Use the 'esp_id' in your get_forecast_mq2 function
    forecast_mq2 = get_forecast_mq2(esp_id)
    return jsonify({"Triple Exponential Smoothing Forecast": forecast_mq2})

@bp.route('/forecast_temperature', methods=['GET'])
def forecast_temperature():
    # Get the 'esp_id' parameter from the query string
    esp_id = request.args.get('esp_id')

    if esp_id is None:
        return jsonify({"error": "Missing 'esp_id' parameter"}), 400

    # Use the 'esp_id' in your get_forecast_temperature function
    forecast_temperature = get_forecast_temperature(esp_id)
    return jsonify({"Triple Exponential Smoothing Forecast": forecast_temperature})

@bp.route('/forecast_pm25', methods=['GET'])
def forecast_pm25():
    # Get the 'esp_id' parameter from the query string
    esp_id = request.args.get('esp_id')

    if esp_id is None:
        return jsonify({"error": "Missing 'esp_id' parameter"}), 400

    # Use the 'esp_id' in your get_forecast_pm25 function
    forecast_pm25 = get_forecast_pm25(esp_id)
    return jsonify({"Triple Exponential Smoothing Forecast": forecast_pm25})


@bp.route('/ispu_co2', methods=['GET'])
def get_ispu_co2_endpoint():
    # Get the 'esp_id' parameter from the query string
    esp_id = request.args.get('esp_id')

    if esp_id is None:
        return jsonify({"error": "Missing 'esp_id' parameter"}, 400)

    # Call the get_ispu_co function to calculate the result
    ispu_co2_result = get_ispu_co2(esp_id)
    return jsonify({"Result ISPU": ispu_co2_result})

@bp.route('/ispu_pm25', methods=['GET'])
def get_ispu_pm25_endpoint():
    # Get the 'esp_id' parameter from the query string
    esp_id = request.args.get('esp_id')

    if esp_id is None:
        return jsonify({"error": "Missing 'esp_id' parameter"}, 400)

    # Call the get_ispu_pm25 function to calculate the result
    ispu_pm25_result = get_ispu_pm25(esp_id)
    return jsonify({"Result ISPU": ispu_pm25_result})

@bp.route('/ispu_co', methods=['GET'])
def get_ispu_co_endpoint():
    # Get the 'esp_id' parameter from the query string
    esp_id = request.args.get('esp_id')

    if esp_id is None:
        return jsonify({"error": "Missing 'esp_id' parameter"}, 400)

    # Call the get_ispu_co function to calculate the result
    ispu_co_result = get_ispu_co(esp_id)
    return jsonify({"Result ISPU": ispu_co_result})

@bp.route('/display', methods=['GET'])
def get_display_endpoint():
    # Call the get_display function to calculate the result
    overall_avg_temperature, overall_avg_humidity, overall_avg_polution = get_display()
    return jsonify({"Temperature": overall_avg_temperature, "Humidity": overall_avg_humidity, "Polution": overall_avg_polution})

@bp.route('/mean', methods=['GET'])
def get_mean_endpoint():
    # Call the get_mean function to calculate the result
    result = get_mean()
    return jsonify({"Result": result})
