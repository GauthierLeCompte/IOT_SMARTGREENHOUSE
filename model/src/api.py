from datetime import datetime, timedelta
import json
from flask import Blueprint, jsonify, request
from src.model import predict_input, predict_input_three_day
from src import db
from src.database.models import Prediction, Prediction_3_Days, Measurement

modelAPI_bl = Blueprint('modelAPI', __name__)


@modelAPI_bl.route('/model/ping', methods=['GET'])
def get():
    print("TOT HIER")
    response = {"phaaung":"pang"}
    return jsonify(response), 200


@modelAPI_bl.route('/model/predict', methods=['POST', 'GET'])
def predict():
    """
    Endpoint for making single prediction
    :return:
    """
    # load request data
    data = json.loads(request.get_json())
    # data = {'DATE': datetime.now().date()}
    data = datetime(data['year'], data['month'], data['day'])

    # predict
    prediction = predict_input(data)
    if prediction is None:
        return jsonify({'success': False, 'status': 'data not found'}), 404

    response = {
        'prediction': prediction,
        'success': True,
        'status': 'Prediction successful'
    }

    # add prediction to db
    if db.session.query(Prediction).filter_by(date=data).first() is None:
        db.session.add(Prediction(data, prediction))
        db.session.commit()

    # remove data older than a month to remain lightweight
    remove_old_data(data)
    return jsonify(response), 200

@modelAPI_bl.route('/model/predict3', methods=['POST', 'GET'])
def predict_three_day():
    """
    Endpoint for making a prediction based on three days since given date
    :return:
    """
    # load request data
    data = json.loads(request.get_json())
    # data = {'DATE':datetime.now().date()}
    data = datetime(data['year'], data['month'], data['day'])

    # predict
    prediction = predict_input_three_day(data)
    response = {
        'prediction': prediction,
        'success': True,
        'status': 'Prediction successful'
    }

    if db.session.query(Prediction_3_Days).filter_by(date=data).first() is None:
        db.session.add(Prediction_3_Days(data, prediction))
        db.session.commit()

    # remove data older than a month to remain lightweight
    remove_old_data(data)
    return jsonify(response), 200

def remove_old_data(date):
    """
    Removes all database entries older than given date. Always called in prediction function in order to keep everything lightweight.
    """
    db.session.query(Prediction).filter(Prediction.date < (date - timedelta(days=31))).delete()
    db.session.query(Measurement).filter(Prediction.date < (date - timedelta(days=31))).delete()
    db.session.query(Prediction_3_Days).filter(Prediction.date < (date - timedelta(days=31))).delete()
    db.session.commit()