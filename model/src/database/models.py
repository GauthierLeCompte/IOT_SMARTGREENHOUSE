from src import db

class Measurement(db.Model):
    """
    Database model representing a measurement received from the greenhouse
    """
    __tableName__ = 'measurement'
    date = db.Column(db.Date, primary_key=True)
    no = db.Column(db.Integer, primary_key=True, autoincrement=True)
    temp_indoor = db.Column(db.Float, nullable=True)
    temp_outdoor = db.Column(db.Float, nullable=True)
    humidity = db.Column(db.Float, nullable=True)
    lamp_status = db.Column(db.Integer, nullable=True)
    rain_status = db.Column(db.Integer, nullable=True)

    def __init__(self, date, temp_in, humidity, lamp, temp_out=None, rain=None):
        self.date = date
        self.temp_outdoor = temp_out
        self.temp_indoor = temp_in
        self.humidity = humidity
        self.lamp_status = lamp
        self.rain_status = rain

    def __repr__(self):
        lamp = "lamps on" if self.lamp_status else "lamps off"
        rain = "raining" if self.rain else "not raining"
        return f'{self.date}: indoor temp: {self.temp_indoor} °C, outdoor temp: {self.temp_outdoor} °C, {self.humidity} % humidity, rain: {rain}, lamps: {lamp}'

    def to_dict(self):
        return {'date': self.date,
                'no': self.no,
                'temp_indoor': self.temp_indoor,
                'temp_outdoor': self.temp_outdoor,
                'humidity': self.humidity,
                'lamp_status': self.lamp_status,
                'rain_status': self.rain_status
                }


class Prediction(db.Model):
    """
    Database model representing a prediction of the electricity cost of a certain day
    """
    __tableName__ = 'prediction'
    date = db.Column(db.Date, primary_key=True)
    prediction = db.Column(db.Float, nullable=False)

    def __init__(self, date, prediction):
        self.date = date
        self.prediction = prediction

    def to_dict(self):
        return {
            'date': self.date,
            'prediction': self.prediction
        }


class Prediction_3_Days(db.Model):
    """
    Database model representing a prediction of the electricity cost of a certain day
    """
    __tableName__ = 'prediction_3_day'
    date = db.Column(db.Date, primary_key=True)
    prediction = db.Column(db.Float, nullable=False)

    def __init__(self, date, prediction):
        self.date = date
        self.prediction = prediction

    def to_dict(self):
        return {
            'date': self.date,
            'prediction': self.prediction
        }