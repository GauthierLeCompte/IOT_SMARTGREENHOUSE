from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import requests
import json
from datetime import datetime, timedelta
import base64
import decodeSensorData


#=======================================================================================================================
#                                              FLASK INITIALIZATION AND SETUP
#=======================================================================================================================

# Create a Flask application and enable CORS
app = Flask(__name__)
CORS(app)

# Register the Blueprint from your api.py
#app.register_blueprint(api_bl)

# Store the greenhouse status as a Python dictionary
greenhouse_status = {
    "temperature": 20,
    "lights": False,
    "humidity": 50,
    "sprinklers": False
}

#=======================================================================================================================
#                                                       API CALLS
#=======================================================================================================================

# Define the GET route for retrieving the greenhouse status
@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify(greenhouse_status)

# Define the POST route for updating the greenhouse status
@app.route('/api/update', methods=['POST'])
def update_status():
    # Get the new desired status from the request JSON
    desired_status = request.get_json()

    # Update the greenhouse status with the new desired status
    for key in desired_status:
        greenhouse_status[key] = desired_status[key]

    return "Updated", 200

# Get prediction from model
@app.route('/api/get-prediction', methods=['GET'])
def get_prediction():
    #base_url = 'https://16bf8e6febf3d5908a8216acba666f71.balena-devices.com'
    base_url = 'http://127.0.0.1:5001'
    endpoint = "/api/predict"
    url = base_url + endpoint
    yesterday = datetime.now().date() - timedelta(days=0)

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
        print(jsonify(response.json()))
        return jsonify(response.json())
    else:
        return jsonify(response.json())

    # Make a request to the /api/predict endpoint
    '''date = '2023-05-28'  # Replace with the desired date
    url = 'http://model:5000/model/predict'
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({'DATE': date})

    response = requests.get(url, headers=headers, data=data)
    print("oke good response?")

    # If the request was successful, return the prediction
    if response.status_code == 200:
        print("oke good response?")
        return jsonify(response.json())
    else:
        return Response("Error when getting prediction", status=response.status_code)'''


#=======================================================================================================================
#                                                CONNECTION TO THE CLOUD
#=======================================================================================================================

base_url = "https://eu1.cloud.thethings.network/api/v3/as/applications/smart-greenhouse-ntg/packages/storage"
headers = {
    "Authorization": "Bearer NNSXS.DWSHILY54MRI6PDGLCUL3YK7A3JJFKHLGCN55XQ.HPQPPV2P3KKHKBUY3KUAAPLEJXK65GSRQZRLYAYFWGZG3RQNQ3NA",
    "Content-Type": "application/json",
}

greenhouse_data = {
    'temperature': '',
    'humidity': '',
    'natural_light': ''
}

hours = []
minutes = []
temp=[]
hum=[]
lights=[]

def deformat_coordinates(encoded_string):
    decoded_string = base64.b64decode(encoded_string).decode('utf-8')
    coordinates = decoded_string.split(';')
    return coordinates

def get_device_data(device_id, data_type="uplink_message"):
    url = f"{base_url}/devices/{device_id}/packages/storage/{data_type}"
    response = requests.get(url, headers=headers)
    return response.json()

def extract_payload_data(payload_item):
    current_dateTime = datetime.now()
    received_at = payload_item['result']['received_at']

    frm_payload = payload_item['result']['uplink_message']['frm_payload']
    temperature, light = deformat_coordinates(frm_payload)
    return {'temperature': temperature, 'light': light}

@app.route('/api/get-application-data', methods=['GET'])
def get_application_data(data_type="uplink_message"):
    current_date = datetime.today().strftime("%Y-%m-%d")
    url = f"{base_url}/{data_type}"
    response = requests.get(url, headers=headers)
    last_timestamp = "2023-05-24T00:00:00Z"

    # base_url2 = 'https://16bf8e6febf3d5908a8216acba666f71.balena-devices.com'
    base_url2 = 'http://127.0.0.1:5001'
    endpoint2 = "/api/upload"
    url2 = base_url2 + endpoint2

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
            if json.loads(data)['result']['received_at'] > last_timestamp:
                last_timestamp = json.loads(data)['result']['received_at']
                values = json.loads(data)['result']["uplink_message"]["frm_payload"]
                temperature, humidity, light = decodeSensorData.decode_sensordata(values)
                greenhouse_data['temperature'] = (temperature)
                greenhouse_data['humidity'] = (humidity)
                greenhouse_data['natural_light'] = (light)

                upload_data = {
                    "TEMP_IN": greenhouse_data['temperature'],
                    "HUMIDITY": greenhouse_data['humidity'],
                    "LIGHT": {"BLUE": light[0],  "RED": light[1]}
                }

                # POST request to upload_data API
                response_upload = requests.post(url=url2, json=upload_data)

                #rint(upload_data)
                if response_upload.status_code == 200:
                    print("Successfully uploaded data")
                else:
                    print(f"Failed to upload data. Status code: {response_upload.status_code}")

                '''if json.loads(data)['result']['received_at'][0:10] == current_date:
                    global hours, minutes, temp, hum, lights
                    minute = int(json.loads(data)['result']['received_at'][14:16])
                    hour = float(json.loads(data)['result']['received_at'][11:13]) + (minute/60)
                    hours.append(hour)
                    temp.append(temperature)
                    hum.append(humidity)
                    lights.append(light[0])'''
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 404

    '''response_text = response.text.replace("}\n{", "},\n{")
    response_text = f"[{response_text}]"
    data = json.loads(response_text)


    test = [extract_payload_data(item) for item in data]
    for item in data:
        current_dateTime = datetime.now()
        received_at = item['result']['received_at']

        if True:
            test.append(extract_payload_data(item))

        year = received_at[0:4]
        month = received_at[5:7]
        day = received_at[8:10]

        print(current_dateTime.year)
        print(current_dateTime.month)
        print(current_dateTime.day)

        print(current_dateTime.date())
        xx = str(current_dateTime.date())

    print(test)
    return data'''


#=======================================================================================================================
#                                                    RUN BACKEND
#=======================================================================================================================

# Run the Flask application on port 5000
if __name__ == '__main__':
    app.run(port=5000, debug=True)
