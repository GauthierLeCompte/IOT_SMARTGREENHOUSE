# Smart Greenhouse Website

This is a Flask-based web application for monitoring and controlling a smart greenhouse. The website displays real-time sensor data and allows users to control various aspects of the greenhouse environment.

## Installation

1. Clone the repository to your local machine:

    git clone https://github.com/GauthierLeCompte/IOT_SMARTGREENHOUSE.git


2. Install the required dependencies by running the `requirements.sh` script:

    ./requirements.sh

## Usage

1. Run the Flask application from the map where app.py is located:

    python3 app.py

2. Open your web browser and navigate to `http://localhost:5000` to access the website.

3. The homepage (`index.html`) displays the current sensor data, control states, and operating mode (manual/automatic).

4. The website automatically fetches sensor data every minute from the TTN API and updates the display. You can also manually trigger data updates by pressing the Reload button.

5. To control the greenhouse environment, switch between manual and automatic modes using the toggle button. In manual mode, you can control the heater, cooler, humidifier, and lights individually. In automatic mode, the control states are adjusted based on the current sensor data.

6. You can access the Coral DevBoard through the prediction buttons. This wil give a cost estimation of the greenhouse.
## File Structure

The project has the following file structure:

- `app.py`: The main Flask application file that handles routing and data processing.
- `decodeSensorData.py`: A module that decodes sensor data received from TTN.
- `requirements.sh`: A shell script that installs the necessary Python dependencies.
- `static/`: A directory where the generated graphs are stored.
- `templates/`: A directory containing HTML template for rendering the website page.
- `templates/index.html`: The main HTML template for the homepage.
- `last_time.txt`: The last timestamp any data was uploaded to the dev board.

## Graphs

The website generates graphs based on the daily sensor data. The graphs are dynamically updated as new data arrives. The generated graphs are saved in the `static/` directory.

- Temperature Graph: Shows the temperature evolution over time.
- Humidity Graph: Displays the humidity evolution over time.
- Lights Graph: Illustrates the changes in natural light intensity over time.


