<template>
  <div id="app">
    <h1>Greenhouse Dashboard</h1>
    <!-- Input fields for desired temperature, lights, humidity, and sprinklers status -->
    <div>
      <label for="temperature">Temperature:</label>
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
    }
  },
  // Used to fetch initial status when component is created
  created() {
    this.getStatus();
  }
};
</script>
