from flask import Flask, render_template, jsonify, request, Response
import requests
import json
import decodeSensorData
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np



hours = []
minutes = []
temp=[]
hum=[]
lights=[]

app = Flask(__name__, static_url_path='/static')

last_timestamp = "2023-05-24T00:00:00Z"
last_file_read_time = "2023-05-24T00:00:00Z"

# Placeholder variables to store greenhouse data and control states
greenhouse_data = {
    'temperature': '',
    'humidity': '',
    'natural_light': ''
}
Prediction = 7
control_states = {
    'heater': False,
    'cooler': False,
    'humidifier': False,
    'lights': False
}
mode = 'manual'

def plotImages():
    global hours, minutes, temp, hum, lights

    # Plotting temperature
    plt.figure()
    plt.plot(hours, temp, marker='o', linestyle='-', color='b')
    plt.xlabel('Time (hours)')
    plt.ylabel('Temperature (Celsius)')
    plt.title('Temperature Evolution')
    plt.xticks(np.arange(min(hours), max(hours) + 1, 1, dtype=int))
    plt.grid(True)
    plt.savefig('static/temperature_graph.png')
    plt.close()

    # Plotting humidity
    plt.figure()
    plt.plot(hours, hum, marker='o', linestyle='-', color='b')
    plt.xlabel('Time (hours)')
    plt.ylabel('Humidity')
    plt.title('Humidity Evolution')
    plt.xticks(np.arange(min(hours), max(hours) + 1, 1, dtype=int))
    plt.grid(True)
    plt.savefig('static/humidity_graph.png')
    plt.close()

    # Plotting lights
    plt.figure()
    plt.plot(hours, lights, marker='o', linestyle='-', color='b')
    plt.xlabel('Time (hours)')
    plt.ylabel('Lights (lux)')
    plt.title('Lights Evolution')
    plt.xticks(np.arange(min(hours), max(hours) + 1, 1, dtype=int))
    plt.grid(True)
    plt.savefig('static/lights_graph.png')
    plt.close()

def parse_timestamp(timestamp):
    last_timestamp = {
        'year': 0,
        'month': 0,
        'day': 0,
        'hour': 0,
        'minute': 0,
        'sec': 0.0
    }

    # Split the timestamp into date and time components
    date_str, time_str = timestamp.split('T')

    # Extract year, month, and day
    last_timestamp['year'], last_timestamp['month'], last_timestamp['day'] = map(int, date_str.split('-'))

    # Extract hour, minute, and second
    time_str = time_str[:-1]  # Remove the trailing 'Z'
    time_parts = time_str.split(':')
    last_timestamp['hour'] = int(time_parts[0])
    last_timestamp['minute'] = int(time_parts[1])
    last_timestamp['sec'] = float(time_parts[2])

    return last_timestamp


@app.route('/')
def index():
    return render_template('index.html',
                           greenhouse_data=greenhouse_data,
                           control_states=control_states,
                           mode=mode)


@app.route('/api/update_prediction')
def update_prediction():
    global Prediction
    base_url = 'https://1881b247ae123a16af96351c18d242cf.balena-devices.com'
    endpoint = "/api/predict"
    url = base_url + endpoint
    yesterday = datetime.now().date() - timedelta(days=2)

    year = int(yesterday.year)
    month = int(yesterday.month)
    day = int(yesterday.day)

    # return data
    data = {'year': year, 'month': month, 'day': day}

    data = json.dumps(data, indent=4, sort_keys=True)

    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, headers=headers, json=data)

    # If the request was successful, return the prediction
    if response.status_code == 200:
        return jsonify(response.json())
    return jsonify(response.json())


@app.route('/api/update_data')
def update_data():

    current_date = date.today().strftime("%Y-%m-%d")
    global last_timestamp
    global last_file_read_time
    url = "https://eu1.cloud.thethings.network/api/v3/as/applications/smart-greenhouse-ntg/packages/storage/uplink_message"
    url+=f"?after=2023-05-23T00:00:00Z"

    base_url2 = 'https://1881b247ae123a16af96351c18d242cf.balena-devices.com'
    endpoint2 = "/api/upload"
    url2 = base_url2 + endpoint2

    api_key = "NNSXS.R5HQMCVUNLBJIKY6TZX2N4DG4VKWRRDBN7THQRY.VAFH6NLJ3WHXASHVEIBSUO2PQB2RDST4GA3JHCPUOVIUOSQXAPTA"

    headers = {
        "Content-Type": "application/list",
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        if response.content == b'':
            greenhouse_data['temperature'] = "null"
            greenhouse_data['humidity'] = "null"
            greenhouse_data['natural_light'] = 'null'
            return jsonify(greenhouse_data)
        data_str = response.content.decode("utf-8")
        data_list = data_str.strip().split("\n")

        # Write each JSON object to a separate file
        for i, data in enumerate(data_list):
            if json.loads(data)['result']['received_at']>last_timestamp:
                last_timestamp = json.loads(data)['result']['received_at']
                values = json.loads(data)['result']["uplink_message"]["frm_payload"]
                temperature, humidity, light = decodeSensorData.decode_sensordata(values)
                greenhouse_data['temperature'] = (temperature)
                greenhouse_data['humidity'] = (humidity)
                greenhouse_data['natural_light'] = (light)

                if json.loads(data)['result']['received_at'][0:10] == current_date:
                    global hours, minutes, temp, hum, lights
                    minute = int(json.loads(data)['result']['received_at'][14:16])
                    hour = float(json.loads(data)['result']['received_at'][11:13]) + (minute/60)
                    hours.append(hour)
                    temp.append(temperature)
                    hum.append(humidity)
                    lights.append(light[0])
                    plotImages()


                if json.loads(data)['result']['received_at'] > last_file_read_time:
                    last_file_read_time = json.loads(data)['result']['received_at']

                    timestamp_data = last_file_read_time[0:10]


                    with open('last_time.txt', 'w') as f:
                        # Write text to the file
                        f.write(last_file_read_time)

                    upload_data = {
                        "DATE" : timestamp_data,
                        "TEMP_IN": greenhouse_data['temperature'],
                        "HUMIDITY": greenhouse_data['humidity'],
                        "LIGHT": {"BLUE": light[0],  "RED": light[1]}
                    }

                    # POST request to upload_data API
                    response_upload = requests.post(url=url2, json=upload_data)

                    if response_upload.status_code == 200:
                        print("Successfully uploaded data")
                    else:
                        print(f"Failed to upload data. Status code: {response_upload.status_code}")

    else:
        # Simulated API call, update the greenhouse data with new values
        greenhouse_data['temperature'] = "null"
        greenhouse_data['humidity'] = "null"
        greenhouse_data['natural_light'] = "null"

    return jsonify(greenhouse_data)


@app.route('/api/update_controls', methods=['POST'])
def update_controls():
    global mode, control_states

    # Get the current mode (manual or automatic)
    mode = request.form.get('mode')

    # Update control states based on the mode and greenhouse data
    if mode == 'manual':
        control_states['heater'] = 'heater' in request.form
        control_states['cooler'] = 'cooler' in request.form
        control_states['humidifier'] = 'humidifier' in request.form
        control_states['lights'] = 'lights' in request.form
    elif greenhouse_data['humidity'] == 'null' or greenhouse_data['temperature'] == 'null' or greenhouse_data[
        'humidity'] == 'null':
        return ''
    elif mode == 'automatic':
        temperature = float(greenhouse_data['temperature'])
        humidity = float(greenhouse_data['humidity'])
        natural_light = float(greenhouse_data['natural_light'][0])
        if control_states['heater']:
            control_states['heater'] = (temperature < 25)
        else:
            control_states['heater'] = (temperature < 20)

        if control_states['cooler']:
            control_states['cooler'] = (temperature > 30)
        else:
            control_states['cooler'] = (temperature > 35)

        if control_states['humidifier']:
            control_states['humidifier'] = (humidity < 60)
        else:
            control_states['humidifier'] = (humidity < 50)

        if control_states['lights']:
            control_states['lights'] = (natural_light < 100)
        else:
            control_states['lights'] = (natural_light < 50)

    return ''

def read_last_file():
    global last_file_read_time
    with open('last_time.txt', 'r') as f:
        # Read the entire content of the file
        buf = f.read()
        if buf != "":
            last_file_read_time = buf


if __name__ == '__main__':
    read_last_file()

    app.run(debug=True)
