import datetime
from sqlalchemy import func

from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
import pandas as pd
import pickle as pkl

from src.preprocessing import preprocess_input_data
from src import db
from src.database.models import Measurement, Prediction


def train_model():
    """
    Trains the model using the training data
    :return:
    """

    # read preprocessed data
    data = pd.read_csv('/usr/src/app/data/data_pp.csv')


    # split data
    costs = data['costs'].copy()
    data.drop(columns=['costs', 'outside_temp', 'rain', 'date', 'heat_c', 'elec_c_high', 'elec_c_low', 'drain_water', 'water_c', 'time', 'Unnamed: 0', 'id'], inplace=True)
    X_train, X_test, y_train, y_test = train_test_split(data, costs, random_state=0, test_size=0.3)

    # train model
    model = GradientBoostingRegressor(random_state=0)
    model.fit(X_train, y_train)

    # store model
    pkl.dump(model, open("/usr/src/app/data/model.pkl", 'wb'))


def test_model():
    """
    Run performance test on model using 30% of learning data
    :return:
    """

    # read preprocessed data
    data = pd.read_csv('/usr/src/app/data/data_pp.csv')

    # split data
    costs = data['costs'].copy()
    data.drop(columns=['costs', 'outside_temp', 'rain', 'date', 'heat_c', 'elec_c_high', 'elec_c_low', 'drain_water', 'water_c', 'time', 'Unnamed: 0', 'id'], inplace=True)
    X_train, X_test, y_train, y_test = train_test_split(data, costs, random_state=0, test_size=0.3)

    # load model
    model = pkl.load(open("/usr/src/app/data/model.pkl", 'rb'))
    predictions = model.predict(X_test)
    print(predictions)
    print(f'MSE: {mean_squared_error(y_test, predictions)}')


def predict_input(date):
    """
    Uses input date to make prediction for that date
    :param date: date of measurements
    :return: prediction
    """

    # load required data from date
    data = db.session.query(Measurement.temp_indoor, Measurement.humidity, Measurement.lamp_status).filter_by(date=date).all()
    if data is None:
        return None

    # translate to dict for accessibility reasons
    data = {'temp_indoor': data[0].temp_indoor, 'humidity': data[0].humidity, 'lamp_status': data[0].lamp_status}
    # preprocess input data
    data = preprocess_input_data(data)


    # load model
    model = pkl.load(open("/usr/src/app/data/model.pkl", 'rb'))
    # predict
    data['prediction'] = model.predict(data)
    return data['prediction'].iloc[0]


def predict_input_three_day(date):
    """
    Makes a bulk prediction for all last three dates starting from given date
    """

    lamp_status_boundary = 75
    day_2 = date - datetime.timedelta(days=1)
    day_3 = day_2 - datetime.timedelta(days=1)

    # load required data from date
    data = db.session.query(func.avg(Measurement.temp_indoor).label('temp_indoor'), func.avg(Measurement.humidity).label('humidity'), func.avg(Measurement.lamp_status).label('lamp_status')).filter(Measurement.date.between(day_3, date)).all()
    if data is None:
        return None
    # translate to dict for accessibility reasons
    data = {'temp_indoor': data[0].temp_indoor, 'humidity': data[0].humidity, 'lamp_status': data[0].lamp_status}
    # find right light status value based on mean, 50 measurements/day
    data['lamp_status'] = 0 if data['lamp_status'] < lamp_status_boundary else 1


    # preprocess input data
    data = preprocess_input_data(data)


    # load model
    model = pkl.load(open("/usr/src/app/data/model.pkl", 'rb'))
    # predict
    data['prediction'] = model.predict(data)
    return data['prediction'].iloc[0]


