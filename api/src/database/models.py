from src import db
from sqlalchemy.sql import func


class Measurement(db.Model):
    __tableName__ = 'measurement'
    date = db.Column(db.Integer, primary_key=True)
    temp_indoor = db.Column(db.Float)
    temp_outdoor = db.Column(db.Float)
    humidity = db.Column(db.Float)
    lamp_status = db.Column(db.Integer)
    rain_status = db.Column(db.Integer)





    def __init__(self, date, temp_out, temp_in, humidity, lamp, rain):
        self.date = date
        self.temp_outdoor = temp_out
        self.temp_indoor = temp_in
        self.humidity = humidity
        self.lamp_status= lamp
        self.rain_status = rain

    def __repr__(self):
        lamp = "lamps on" if self.lamp_status else "lamps off"
        rain = "raining" if self.rain else "not raining"
        return f'{self.date}: indoor temp: {self.temp_indoor} °C, outdoor temp: {self.temp_outdoor} °C, {self.humidity} % humidity, rain: {rain}, lamps: {lamp}'




