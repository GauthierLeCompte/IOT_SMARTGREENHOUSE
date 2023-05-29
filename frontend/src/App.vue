<template>
  <div id="app">
    <h1>Greenhouse Dashboard</h1>
    <!-- Input fields for desired temperature, lights, humidity, and sprinklers status -->
    <button @click="getPrediction">Get Prediction</button>
    <div v-if="prediction">Prediction: {{ prediction }}</div>

    <button @click="refreshData">Refresh Data()</button>

    <div>
      <label for="temperature">Temperatureeeeeeee:</label>
      <input type="number" id="temperature" v-model.number="desiredStatus.temperature" />
    </div>
    <div>
      <label for="lights">Lights:</label>
      <input type="checkbox" id="lights" v-model="desiredStatus.lights" />
    </div>
    <div>
      <label for="humidity">Humidity:</label>
      <input type="number" id="humidity" v-model.number="desiredStatus.humidity" />
    </div>
    <div>
      <label for="sprinklers">Sprinklers:</label>
      <input type="checkbox" id="sprinklers" v-model="desiredStatus.sprinklers" />
    </div>
    <!-- Button for updating the greenhouse status -->
    <button @click="updateStatus">Update</button>
    <!-- Display the current greenhouse status -->
    <h2>Current Greenhouse Status</h2>
    <pre>{{ greenhouseStatus }}</pre>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      greenhouseStatus: {},
      prediction: null,
      desiredStatus: {
        temperature: 0,
        lights: false,
        humidity: 0,
        sprinklers: false
      }
    };
  },
  methods: {
    // Fetch the current greenhouse status from the Flask backend
    async getStatus() {
      const response = await axios.get('http://127.0.0.1:5000/api/status');
      this.greenhouseStatus = response.data;
    },
    // Update the greenhouse status in the Flask backend
    async updateStatus() {
      console.log("Updating status with:", this.desiredStatus);
      await axios.post('http://127.0.0.1:5000/api/update', this.desiredStatus);
      this.getStatus();
    },
    async refreshData() {
      const response = await axios.get('http://127.0.0.1:5000/api/get-application-data')
      console.log(response.data)
    },
    async getPrediction() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/get-prediction')
        console.log(response.data)
        this.prediction = response.data
      } catch (error) {
        console.error('Error occurred:', error);
        if (error.response) {
            // The request was made and the server responded with a status code that falls out of the range of 2xx
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response.headers);
        } else if (error.request) {
            // The request was made but no response was received
            console.log(error.request);
        } else {
            // Something happened in setting up the request that triggered an Error
            console.log('Error', error.message);
        }
        this.prediction = 'An error occurred while fetching the prediction.';
      }
    }
  },
  // Used to fetch initial status when component is created
  created() {
    this.getStatus();
  }
};
</script>
