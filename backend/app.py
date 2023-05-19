from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

# Create a Flask application and enable CORS
app = Flask(__name__)
CORS(app)

# Store the greenhouse status as a Python dictionary
greenhouse_status = {
    "temperature": 20,
    "lights": False,
    "humidity": 50,
    "sprinklers": False
}

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


@app.route('/app-endpoint', methods=['GET', 'POST'])
def app_endpoint():
    # This code will run when a user makes a GET or POST request to "/app-endpoint"
    response = requests.get('http://<api-server>/api/predict')
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"error": "Unable to get prediction"}), response.status_code


# Run the Flask application on port 5000
if __name__ == '__main__':
    app.run(port=5000, debug=True)
