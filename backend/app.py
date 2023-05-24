from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import requests
import json
from datetime import datetime
import base64


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
    # Make a request to the /api/predict endpoint
    response = requests.get('http://127.0.0.1:5001/api/predict')
    print(response)

    # If the request was successful, return the prediction
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return Response("Error when getting prediction", status=response.status_code)


#=======================================================================================================================
#                                                CONNECTION TO THE CLOUD
#=======================================================================================================================

base_url = "https://eu1.cloud.thethings.network/api/v3/as/applications/smart-greenhouse-ntg/packages/storage"
headers = {
    "Authorization": "Bearer NNSXS.DWSHILY54MRI6PDGLCUL3YK7A3JJFKHLGCN55XQ.HPQPPV2P3KKHKBUY3KUAAPLEJXK65GSRQZRLYAYFWGZG3RQNQ3NA",
    "Content-Type": "application/json",
}

def get_device_data(device_id, data_type="uplink_message"):
    url = f"{base_url}/devices/{device_id}/packages/storage/{data_type}"
    response = requests.get(url, headers=headers)
    return response.json()

def get_application_data(data_type="uplink_message"):
    url = f"{base_url}/{data_type}"
    response = requests.get(url, headers=headers)
    return response.json()


#=======================================================================================================================
#                                                    RUN BACKEND
#=======================================================================================================================

# Run the Flask application on port 5000
if __name__ == '__main__':
    app.run(port=5000, debug=True)
