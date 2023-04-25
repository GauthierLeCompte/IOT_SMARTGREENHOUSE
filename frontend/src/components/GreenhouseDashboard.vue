<template>
  <div class="jumbotron vertical-center">
  <div class="container">
    <!-- bootswatch CDN -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/lux/bootstrap.min.css"
          integrity="sha384-9+PGKSqjRdkeAU7Eu4nkJU8RFaH8ace8HGXnkiKMP9I9Te0GJ4/km3L1Z8tXigpG"
          crossorigin="anonymous">
    <div class="row">
      <div class="col-sm-12">
        <h1>Greenhouse Control Dashboard 🏡</h1>
        <hr><br>

        <!-- Alert message when somethings has changed -->
        <label>Desired temperature:</label>
        <input type="number" v-model="temperature"/>
        <button type="button" class="btn">set</button><br><br>

        <label>Set Lights:</label>
        <div class="btn-group" role="group">
          <button type="button" class="btn btn-success">On</button>
          <button type="button" class="btn btn-danger">Off</button>
        </div><br><br>

        <label>Desired humidity:</label>
        <input type="number" v-model="temperature"/>
        <button type="button" class="btn">set</button><br><br>

        <label>Set sprinklers:</label>
        <div class="btn-group" role="group">
          <button type="button" class="btn btn-success">On</button>
          <button type="button" class="btn btn-danger">Off</button>
        </div><br><br>
        <br><br>
        <br><br>

        <h6>Current status greenhouse</h6>
        <table class="table table-hover">
          <thead>
            <tr>
              <!-- table header cells -->
              <th scope="col">Temperature</th>
              <th scope="col">Lights</th>
              <th scope="col">Humidity</th>
              <th scope="col">Soil Moisture level</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>21°</td>
              <td>On</td>
              <td>90%</td>
              <td>High</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
  </div>
</template>

<script>
export default {
  name: "GreenhouseDashboard"
}
</script>

<style scoped>

</style>