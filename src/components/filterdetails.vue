<template>
  <div class = "filterdetails container">

    <button type="button" class="btn btn-danger" style="float: right;" v-on:click="logout">Logout</button>
    <h4><b> Hello {{userid}} !</b></h4>

    <div class="page-header">
        <center><h1>Weather Data Filter Screen</h1></center>
    </div>

    <!-- popup -->
    <vue-modaltor :visible="isPopup" @hide="isPopup = false">
      <div id="popupdiv" ref="popudiv" class="customscroll" style="height:680px;overflow-y:auto;overflow-x:hidden;">
        <div class="page-header">
          <h3 >Location</h3>
        </div>
        <div class="alert label-primary" role="alert">
          <strong>{{fullLocation}}</strong>
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
      <center><button type="button" class="btn btn-success" v-on:click="isPopup = false">Got It!</button></center>
    </vue-modaltor>


    <div >
      <center><div class="loader" v-if="isLoader" style="z-index:20000;" ></div></center>
    <div class="table-responsive" v-show="!isLoader">

            <table style="display:block;" class="table table-striped  table-hover">
              <thead >
                <tr style="text-align:center;">
                  <th>Location
                    <br/>
                    <input type="text" v-model="location" class ="form-control" placeholder="State or Zipcode or City"/>
                  </th>
                  <th>Date (Month dd,yyyy)
                    <br/>
                    <input type="text" v-model="date" class ="form-control" placeholder="Month or dd or yyyy"/>
                  </th>
                  <th>Average Temperature<br/> Of The Day (in F)
                    <br/>
                    <input type="number" v-model="avgTemp" class ="form-control" placeholder="Filter Temerature"/>
                  </th>
                  <th>Average Wind Speed<br/> Of The Day (in MPH)
                    <br/>
                    <input type="number" v-model="avgWind" class ="form-control" placeholder="Filter Wind Speed"/>
                  </th>
                  <th>Weather Condition at<br/> 16:00 Local Time
                    <br/>
                  <!--  <input type="text" v-model="cond" class ="form-control" placeholder="Filter Condition"/>-->
                    <select v-model="cond" class ="form-control" placeholder="Filter Condition">
                      <option v-for="option in condList" v-bind:value="option">
                        {{ option }}
                      </option>
                    </select>
                  </th>
                </tr>
              </thead>
              <tbody class="customscroll" style="overflow-y:auto; height:500px;width:100%;display: block;table-layout:fixed">
                <tr style="display:table;width:100%;table-layout:fixed;text-align:center"

                          v-for="obj in filterBy(filterBy(filterBy(filterBy(filterBy(
                          jsonList,location,'location.city','location.state','location.zip'),
                          date,'history.date.pretty'),
                          avgTemp,'history.dailysummary.0.meantempi'),
                          avgWind, 'history.dailysummary.0.meanwindspdi'),
                          cond, 'history.observations.16.conds')
                            " v-on:click="generatePopup(obj.location.zip)" >
                  <td>{{obj.location.city + ", " + obj.location.state + " - "
                         + obj.location.zip + ", " +obj.location.country_name }}</td>
                  <td>{{obj.history.date.pretty}}</td>
                  <td>{{obj.history.dailysummary[0].meantempi + " F"}}</td>
                  <td>{{obj.history.dailysummary[0].meanwindspdi + " MPH"}}</td>
                  <td v-if="obj.history.observations[16] != undefined">{{obj.history.observations[16].conds}}</td>
                  <td v-else>undefined</td>
                </tr>
              </tbody>
            </table>

            </div>
          </div>
            <center><button type="button" class="btn btn-info" v-on:click="clearFilters">Clear Filters</button></center>
  </div>
</template>
<script>
  import Vue from 'vue'
  import Vue2Filters from 'vue2-filters'
  import VueModalTor from 'vue-modaltor'
  import Login from '@/components/Login'
  import axios from 'axios';
  import VueSession from 'vue-session'

  Vue.use(VueSession);
  Vue.use(VueModalTor);
  Vue.use(Vue2Filters);

  export default {
    name: 'filterdetails',
    data() {
      return{
        jsonList: '',
        location: '',
        date:'',
        avgTemp: '',
        avgWind: '',
        cond: '',
        condList: [''],
        clickRowZip: '',
        isPopup: false,
        obsList: [],
        summaryList: [],
        fullLocation: '',
        highTemp: '',
        highOn: '',
        lowTemp: '',
        lowOn: '',
        showUser: false,
        isLoader: true
      }
    },
    props: {
      userid: {
        type: String,
        default: 'Vue!'
      }
    },
    methods: {
      // To Clear all the filters
      clearFilters: function(){
        this.location = '';
        this.date = '';
        this.avgTemp = '';
        this.avgWind = '';
        this.cond = '';
        return;
      },
      // Logout of current session
      logout: function(){
        this.$session.destroy();
        this.$router.push({ name: 'Login'});
      },
      // To generate pop up on click of a row
      generatePopup: function(zip){
        this.clickRowZip = zip;
        this.isPopup = true;
        var found = false;
        this.obsList = [];
        this.summaryList = [];
        for(var i=0; i<this.jsonList.length; i++){
          var obj = this.jsonList[i];
          if(obj.location != undefined){
            if(obj.location.zip == this.clickRowZip){
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

              this.fullLocation = obj.location.city + ", " + obj.location.state + ", "
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
      }
    },
    beforeCreate: function() {
      //Handling browser buttons.
      if (!this.$session.exists()) {
        this.$router.push({ name: 'Login'});
        return;
      }
      // To load the weather data and populate the condition dropdown filter
      this.isLoader=true;
      axios.get('static/WeatherData.json')
        .then((res) => {
          this.jsonList = res.data;
          for(var i=0; i<this.jsonList.length; i++){
            var obj = this.jsonList[i];
            if(obj.history.observations.length > 16)
            {
              var pushObj = ''
              pushObj = obj.history.observations[16].conds;
              if(!this.condList.includes(pushObj))
                this.condList.push(pushObj);
            }
          }
          this.isLoader=false;
        })

    }
  };
</script>
<style scoped>

tbody tr:nth-child(even) {
  background-color: #aee3ef;
}

tbody tr:nth-child(odd) {
  background-color: #ffffff;
}

tbody tr:nth-child(even):hover {
  background-color: #5496b5;
}
tbody tr:nth-child(odd):hover {
  background-color: #5496b5;
}
.customscroll::-webkit-scrollbar {
    width: 4px;
}
.customscroll::-webkit-scrollbar-track {
    background-color: #e6e6e6;
    border-width: 0;
}
.customscroll::-webkit-scrollbar-thumb {
    border-radius: 0px;
    background-color: #000080;
    border-style: solid;
    border-color: transparent;
    border-width: 0px;
    background-clip: padding-box;
}
/* hidden elements */
.customscroll::-webkit-scrollbar-button,
.customscroll::-webkit-scrollbar-track-piece,
.customscroll::-webkit-scrollbar-corner,
.customscroll::-webkit-resizer { display: none; }

.loader {
  border: 5px solid #4d4d4d;
  border-radius: 50%;
  border-top: 5px solid #3498db;
  width: 120px;
  height: 120px;
  -webkit-animation: spin 2s linear infinite; /* Safari */
  animation: spin 2s linear infinite;
}

/* Safari */
@-webkit-keyframes spin {
  0% { -webkit-transform: rotate(0deg); }
  100% { -webkit-transform: rotate(360deg); }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
