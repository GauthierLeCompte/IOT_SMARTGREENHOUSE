import requests
from flask import Blueprint, jsonify, Request
from os import path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
from src.parameters import PRICE_HEAT, PRICE_ELEC_LOW, PRICE_ELEC_HIGH, GREENHOUSE_SIZE


model_bl = Blueprint('model', __name__)


@model_bl.route('/model/ping', methods=['GET'])
def get():
    response={"pong":"pong"}
    return jsonify(response), 200


@model_bl.route('/model/predict', methods=['POST'])
def predict():
    """
    Endpoint for making predictions

    Data might need to come from database in later version
    :return:
    """
    # load request data
    data = Request.get_json()
    if data is None:
        return jsonify({'success': False, 'status': 'No input data received'}), 400

    # predict
    prediction = predict_input(data)
    response = {
        'prediction': prediction,
        'success': True,
        'status': 'Prediction successful'
    }

    return jsonify(response), 200



def preprocess_conditions():
    """
    Preprocesses the conditions dataset
    :return:
    """
    conditions = pd.read_csv("/usr/src/app/data/conditions.csv")
    conditions['time'] = pd.to_datetime(conditions['time'], unit='D', origin='1899-12-30').dt.date
    all_dates = conditions['time'].unique().tolist()
    print(len(all_dates))

    new_df = pd.DataFrame(columns=['date', 'temperature', 'humidity', 'outside_temp', 'lamp', 'rain'])
    for date in all_dates:
        rows = conditions[conditions["time"] == date]
        lamp = 1 if len(rows[rows['lamp_status'] == 1]) >=  len(rows[rows['lamp_status'] == 0]) else 0
        new_df.loc[len(new_df)] = [date, rows["temperature"].mean(), rows['humidity'].mean(), rows['outside_temp'].mean(), lamp, rows['rain'].mean()]

    new_df.to_csv('/usr/src/app/data/conditions_pp.csv')
    return new_df


def preprocess_resources():
    """
    Preprocesses the resources dataset
    :return:
    """
    resources = pd.read_csv("/usr/src/app/data/resources.csv")
    resources['date'] = pd.to_datetime(resources['time'], unit='D', origin='1899-12-30').dt.date
    resources.to_csv('/usr/src/app/data/resources_pp.csv')
    print(resources.describe())
    return resources

def preprocess_data():
    """
    Preprocesses training dataset
    :return:
    """
    conditions = None
    resources = None
    if not path.isfile('/usr/src/app/data/conditions_pp.csv'):
        conditions = preprocess_conditions()
        resources = preprocess_resources()
    else:

        conditions = pd.read_csv('/usr/src/app/data/conditions_pp.csv')
        resources = pd.read_csv("/usr/src/app/data/resources_pp.csv")

    #combine dataframes
    data = pd.merge(conditions, resources)
    data = data.rename(columns={"Unnamed: 0": 'ID'})
    # calculate costs
    data['costs'] = (data["heat_c"] * PRICE_HEAT + data["elec_c_high"] * PRICE_ELEC_HIGH + data["elec_c_low"] * PRICE_ELEC_LOW) * GREENHOUSE_SIZE

    # label encode
    date_encoder = LabelEncoder()
    data["date"] = date_encoder.fit_transform(data["date"])


    data.to_csv('/usr/src/app/data/data_pp.csv')


def train_model():
    """
    Trains the model using the training data
    :return:
    """

    # read preprocessed data
    data = pd.read_csv('/usr/src/app/data/data_pp.csv')


    # split data
    costs = data['costs'].copy()
    data.drop(columns=['costs'], inplace=True)
    X_train, X_test, y_train, y_test = train_test_split(data, costs, random_state=0, test_size=0.3)

    # train model
    model = GradientBoostingRegressor(random_state=0)
    model.fit(X_train,y_train)

    # store model
    pickle.dump(model, open("/usr/src/app/data/model.pkl", 'wb'))

def test_model():
    """
    Run performance test on model using 30% of learning data
    :return:
    """

    # read preprocessed data
    data = pd.read_csv('/usr/src/app/data/data_pp.csv')

    # split data
    costs = data['costs'].copy()
    data.drop(columns=['costs'], inplace=True)
    X_train, X_test, y_train, y_test = train_test_split(data, costs, random_state=0, test_size=0.3)

    # load model
    model = pickle.load(open("/usr/src/app/data/model.pkl", 'rb'))
    predictions = model.predict(X_test)
    print(predictions)
    print(f'MSE: {mean_squared_error(y_test, predictions)}')



def preprocess_input_data(data):
    """
    Translates the input data to suitable format
    :param data:
    :return:
    """
    #TODO: Translate input data to correct format for predictive model
    return data


def predict_input(data):
    """
    Uses input data to make prediction
    :param data: input data from measurements
    :return: prediction
    """

    # preprocess input data
    data = preprocess_input_data(data)
    # load model
    model = pickle.load(open("/usr/src/app/data/model.pkl", 'rb'))
    # predict
    prediction = model.predict(data)
    return prediction





