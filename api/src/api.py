import requests
from flask import Blueprint, jsonify


api_bl = Blueprint('api', __name__)


@api_bl.route('/api/ping', methods=['GET'])
def get():
    response={"pong":"pong"}
    return jsonify(response), 200



"""
BELOW IS AN EXAMPLE FUNCTION FOR LATER REFERENCE @GAUTHIER
"""
@api_bl.route('/api/predict', methods=['GET', 'POST'])
def request_prediction():
    print("in dataaaaa")
    data = {'time': 459999,'temp': 21.5, 'outside_temp': 16.2, 'humidity': 51.8, 'lamp_status': 1, 'rain': 0} # example

    r = requests.post(url="http://iot_model/model/predict", data=data).json()

    response = {"success": True, 'prediction': r}
    return jsonify(data), 200
