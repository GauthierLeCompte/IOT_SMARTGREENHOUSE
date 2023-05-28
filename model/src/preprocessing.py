import pandas as pd
from os import path
from src.parameters import PRICE_HEAT, PRICE_ELEC_LOW, PRICE_ELEC_HIGH, GREENHOUSE_SIZE
from sklearn.preprocessing import LabelEncoder


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


def preprocess_input_data(data):
    """
    Translates the input data from sqlalchemy to pandas input format
    :param data: sqlalchemy input
    :return: pandas df
    """

    new_df = pd.DataFrame(columns=['temperature', 'humidity', 'lamp'])
    new_df.loc[len(new_df)] = [data['temp_indoor'], data['humidity'], data['lamp_status']]

    return new_df