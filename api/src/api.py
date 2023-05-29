import requests
import json
from src import db
from src.database.models import Measurement, Prediction, Prediction_3_Days
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request

api_bl = Blueprint('api', __name__)

PREDICTION_VALUES = ['TEMP_IN', 'HUMIDITY', 'LAMP_STATUS']

@api_bl.route('/api/ping', methods=['GET'])
def get():
    response = {"please": "werk AUUUBBB 222"}
    print("yellow")
    return jsonify(response), 200


@api_bl.route('/api/connect', methods=['GET'])
def connect_to_model():
    r = requests.get(url="http://model:5000/model/ping").json()
    return r, 200


@api_bl.route('/api/upload', methods=['GET', 'POST'])
def upload_data():
    """
    Receives measurement data from greenhouse and stores in database
    Data should be of format:
    {DATE, TEMP_IN, TEMP_OUT, HUMIDITY, LAMP_STATUS, RAIN_STATUS}
    Order does not matter, None is allowed
    """

    # load data from request
    data = request.get_json()
    '''if PREDICTION_VALUES not in data.keys():
        return jsonify({'success': False, 'status': 'No input data received'}), 400'''

    # dummy data below, outcomment lines above
    # data = {'TEMP_IN': 15.3, 'HUMIDITY': 50.6, 'LIGHT': {'BLUE': 60, 'RED': 17}}

    # load date
    date = datetime.now().date()

    # load TEMP OUT and RAIN_STATUS from weather api
    rain_status = None
    temp_out = None
    # convert light information to lamp status
    lamp_status = 1
    if data['LIGHT']['BLUE'] > 50 or data['LIGHT']['RED'] > 50:
        lamp_status = 0

    # add new measurement to database
    db.session.add(Measurement(date, data['TEMP_IN'], data['HUMIDITY'], lamp_status))
    db.session.commit()

    response = {'success': True, 'message': 'Successfully uploaded measurement'}
    return jsonify(response), 200


@api_bl.route('/api/predict', methods=['GET', 'POST'])
def request_prediction():
    """
    Receives a date in the request and makes prediction for that date. Then stores prediction.
    """
    # load date from request data
    data = json.loads(request.get_json())
    #data = {'DATE': datetime.now().date()}

    if not (data['year']):
        return jsonify({'success': False, 'status': 'No input data received'}), 404

    # json dump due to date
    data = json.dumps(data, indent=4, sort_keys=True)

    # send http request to model container
    r = requests.post(url="http://model:5000/model/predict", json=data).json()

    if r['success'] == False:
        return jsonify(r), 404
    else:
        response = {"success": True, 'prediction': r['prediction']}
        return jsonify(response), 200


@api_bl.route('/api/predict3', methods=['GET', 'POST'])
def request_three_day_prediction():
    """
    Receives a date in the request and makes a combined prediction for the last three dates. Then stores prediction.
    """
    # load date from request data
    data = request.get_json()
    # data = {'DATE': datetime.now().date()}

    if not (data['year']):
        return jsonify({'success': False, 'status': 'No input data received'}), 404

    # json dump due to date
    data = json.dumps(data, indent=4, sort_keys=True)

    # send http request to model container
    r = requests.post(url="http://model:5000/model/predict3", json=data).json()

    if r['success'] == False:
        return jsonify(r), 404
    else:
        response = {"success": True, 'prediction': r['prediction']}
        return jsonify(response), 200


@api_bl.route('/api/measurements', methods=['GET'])
def load_measurements():
    """
    Loads all predictions from database
    """
    # load all measurements from db
    measurements = db.session.query(Measurement).all()
    if not measurements:
        return jsonify({'success': False}), 404

    # list measurements
    results = []
    for measurement in measurements:
        results.append(measurement.to_dict())

    return jsonify({'success': True, 'measurements': results}), 200


@api_bl.route('/api/predictions', methods=['GET'])
def load_all_predictions():
    """
    Loads all predictions from database
    """

    # load all predictions from db
    predictions = db.session.query(Prediction).all()
    if not predictions:
        return jsonify({'success': False}), 404


    results = []
    for prediction in predictions:
        results.append(prediction.to_dict())

    return jsonify({'success': True, 'predictions': results}), 200


@api_bl.route('/api/predictions/<int:date>', methods=['GET'])
def load_prediction(date):
    """
    Loads all prediction from specified date from database
    """
    # load all predictions from db
    prediction = db.session.query(Prediction).filter_by(date=date).first()
    if not prediction:
        return {'success': False, 'status': 'Missing input parameter'}, 404

    return {'success': True, 'prediction': prediction.to_dict()}, 200


@api_bl.route('/api/predictions3', methods=['GET'])
def load_all_3_day_predictions():
    """
    Loads all 3-day predictions from database
    """

    # load all predictions from db
    predictions = db.session.query(Prediction_3_Days).all()
    if not predictions:
        return jsonify({'success': False}), 404


    results = []
    for prediction in predictions:
        results.append(prediction.to_dict())

    return jsonify({'success': True, 'predictions': results}), 200

