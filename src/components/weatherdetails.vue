<template>
  <div class = "weatherdetails container">
    <button type="button" style="float: right;" class="btn btn-danger" v-on:click="logout">Logout</button>
    <h4><b> Hello {{userid}} !</b></h4>
    <div class="page-header">
        <center><h1>Weather Screen</h1></center>
    </div>
    <p><b> Get Weather Data using :</b></p>
    <div class="custom-control custom-radio">
      <input type="radio" id="currLocationRadio" name="locationRadio" v-on:click="currLocationClick" class="custom-control-input">
      <label class="custom-control-label" for="currLocationRadio"> Current Location</label>
    </div>
    <div class="custom-control custom-radio">
      <input type="radio" id="customLocationRadio" name="locationRadio" v-on:click="isCustom=true" class="custom-control-input">
      <label class="custom-control-label" for="customLocationRadio"> Custom Location</label>
    </div>
    <form v-on:submit = "getData(zipcode)" v-show="isCustom" class="form-inline">
      <input type="number" v-model="zipcode" class ="form-control" placeholder="Enter Custom Zipcode" required autofocus/>

      <input type="submit" class="btn btn-primary mb-2" value="Go">
    </form>
    <br/>
    <div v-show="showError">
      <div class="alert alert-danger" role="alert">
        <strong>Zipcode {{zipcodeSearch}} Not Found</strong> Change zipcode and try submitting again.
      </div>
    </div>
    <div v-show="showDetails">
      <div class="page-header">
        <h3>Location</h3>
      </div>
      <div class="alert label-primary" role="alert">
        <strong>{{location}}</strong>
      </div>
      <div class="page-header">
        <h3>Weather Observations</h3>
      </div>
      <div class="row">
        <div class="col-sm-4" v-for="obs in obsList">
          <div class="panel panel-primary">
            <div class="panel-heading">
              <h3 class="panel-title">{{obs.date}}</h3>
            </div>
            <div class="panel-body">
              <p>Time: <b>16:00 local time</b></p>
              <h4><b>{{obs.condition}}</b></h4>
              <p>Temprature: <b>{{obs.temperature}}</b></p>
              <p>Humidity: <b>{{obs.humidity}}</b></p>
              <p>Wind Speed: <b>{{obs.wind}}</b></p>
            </div>
          </div>
        </div>
      </div>
      <div class="page-header">
        <h3>Full Day Summary</h3>
      </div>
      <div class="row">
        <div class="col-sm-4" v-for="obs in summaryList">
          <div class="panel panel-primary">
            <div class="panel-heading">
              <h3 class="panel-title">{{obs.sDate}}</h3>
            </div>
            <div class="panel-body">
              <p>Average Temperature: <b>{{obs.meanTemp}}</b></p>
              <p>Temprature (max/min): <b>{{obs.sTemperature}}</b></p>
              <p>Humidity (max/min): <b>{{obs.sHumidity}}</b></p>
              <p>Wind Speed (max/min): <b>{{obs.sWind}}</b></p>
            </div>
          </div>
        </div>
      </div>
      <div class="page-header">
        <h3>Record Statistics</h3>
      </div>
      <div class="row">
        <div class="col-sm-6">
          <div class="panel panel-primary">
            <div class="panel-heading">
              <h3 class="panel-title">Highest Temperature</h3>
            </div>
            <div class="panel-body">
              <p>High: {{highTemp}}</p>
              <p>Record Year: {{highOn}}</p>
            </div>
          </div>
        </div>
        <div class="col-sm-6">
          <div class="panel panel-primary">
            <div class="panel-heading">
              <h3 class="panel-title">Lowest Temperature</h3>
            </div>
            <div class="panel-body">
              <p>Low: {{lowTemp}}</p>
              <p>Record Year: {{lowOn}}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <button type="button" style="float: right;" class="btn btn-success" v-on:click="proceed">Proceed</button>
<br/><br/>
  </div>
</template>

<script src="https://maps.googleapis.com/maps/api/js?sensor=false" type="text/javascript"></script>
<script src="/assets/gmap3.js?body=1" type="text/javascript"></script>

<script>
//  import weatherjson from '../../WeatherData.json'
  import axios from 'axios';
  import filterdetails from '@/components/filterdetails'
  import Login from '@/components/Login'
  import VueGeolocation from 'vue-browser-geolocation'
  import LatlonToZip from 'latlng-to-zip'
  import Vue from 'vue'
  import VueSession from 'vue-session'

  Vue.use(VueSession);
  Vue.use(VueGeolocation);

  export default {
    name: 'weatherdetails',
    data() {
      return {
        //userid: '',
        isCustom: false,
        showDetails: false,
        showError: false,
        jsonList: '' ,
        zipcodeSearch: '',
        zipcode: '',
        currZipcode: '14215',
        obsList: [],
        summaryList: [],
        location: '',
        highTemp: '',
        highOn: '',
        lowTemp: '',
        lowOn: ''

      }
    },
    props: {
      userid: {
        type: String,
        default: 'Vue!'
      }
    },
    methods: {
      // To get weather data of a zip code
      getData: function(zipSearch){
        this.zipcodeSearch = zipSearch;
        var found = false;
        this.obsList = [];
        this.summaryList = [];
        for(var i=0; i<this.jsonList.length; i++){
          var obj = this.jsonList[i];
          if(obj.location != undefined){
            if(obj.location.zip == this.zipcodeSearch){
              found = true;
              var obsObject= {
                date:'',
                temperature:'',
                condition: '',
                humidity: '',
                wind: ''
              };
              var summaryObject= {
                meanTemp: '',
                sDate: '',
                sTemperature: '',
                sHumidity: '',
                sWind: ''
              };

              this.location = obj.location.city + ", " + obj.location.state + ", "
                              + obj.location.country_name + ", zipcode - " + obj.location.zip;
              obsObject.date = obj.history.date.pretty;
              obsObject.temperature = (obj.history.observations.length <= 16)?"undefined":(obj.history.observations[16].tempi + "F (" +
                                            obj.history.observations[16].tempm + "C)");
              obsObject.condition = (obj.history.observations.length <= 16)?"condition undefined":(obj.history.observations[16].conds);
              obsObject.humidity = (obj.history.observations.length <= 16)?"undefined":(obj.history.observations[16].hum + "%");
              obsObject.wind = (obj.history.observations.length <= 16)?"undefined":(obj.history.observations[16].wspdi + " MPH");
              this.obsList.push(obsObject);
              summaryObject.sDate = obj.history.date.pretty;
              summaryObject.meanTemp = (obj.history.dailysummary.length <= 0)?"undefined":(obj.history.dailysummary[0].meantempi + "F");
              summaryObject.sTemperature = (obj.history.dailysummary.length <= 0)?"undefined":(obj.history.dailysummary[0].maxtempi +
                                            "F / " + obj.history.dailysummary[0].mintempi + "F");
              summaryObject.sHumidity = (obj.history.dailysummary.length <= 0)?"undefined":(obj.history.dailysummary[0].maxhumidity +
                                            "% / " + obj.history.dailysummary[0].minhumidity + "%");
              summaryObject.sWind = (obj.history.dailysummary.length <= 0)?"undefined":(obj.history.dailysummary[0].maxwspdi +
                                            " MPH / " + obj.history.dailysummary[0].minwspdi + " MPH");
              this.summaryList.push(summaryObject);
              this.highTemp = obj.almanac.temp_high.record.F + "F / " + obj.almanac.temp_high.record.C + "C";
              this.highOn = obj.almanac.temp_high.recordyear;
              this.lowTemp = obj.almanac.temp_low.record.F + "F / " + obj.almanac.temp_low.record.C + "C";
              this.lowOn = obj.almanac.temp_low.recordyear;
            }
          }
        }
        if(!found)
        {
          this.showDetails = false;
          this.showError = true;
        }
        else{
          this.showDetails = true;
          this.showError = false;
        }

      },
      currLocationClick: function(){
        this.isCustom=false;
        //this.zipcode = this.currZipcode;
        this.getData(this.currZipcode);
      },
      // To proceed to next screen.
      proceed: function(){
        this.$router.push({ name: 'filterdetails', params: { userid: this.userid }});
      },
      // to logout of current session
      logout: function(){
        this.$session.destroy();
        this.$router.push({ name: 'Login'});
      }
    },
    beforeCreate: function() {
      //Handling browser buttons.
      if (!this.$session.exists()) {
        this.$router.push({ name: 'Login'});
        return;
      }
      // To get Current location zip code
      this.$getLocation()
        .then(coordinates => {
          var latitude = coordinates.lat;
          var longitude = coordinates.lng;
          LatlonToZip({latitude, longitude})
            .then(zip => {
              this.currZipcode = zip
            })
            .catch(err => err);
        });
        // To load the weather data
        axios.get('static/WeatherData.json')
          .then((res) => {
            this.jsonList = res.data;
          })
    }
  };
</script>
