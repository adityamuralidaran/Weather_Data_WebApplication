<template>
    <div class = "Login container">
      <form v-on:submit = "authenticate" class="form-signin">
      <h2 class="form-signin-heading"><center> Login </center></h2>
      <input type="text" v-model="userid" class ="form-control" placeholder="Enter User ID" required autofocus/>
      <br/>
      <input type="password" v-model="pwd" class ="form-control" placeholder="Enter Password" required/>
      <br/>
      <input type="submit" class="btn btn-lg btn-primary btn-block" value="submit">
      </form>
      <div v-show="loginError" >
        <div class="alert alert-danger" role="alert">
          <center><strong>Invalid User ID or Password</strong></center>
        </div>
      </div>
    </div>
</template>

<script>
import weatherdetails from '@/components/weatherdetails'
import VueSession from 'vue-session'
import axios from 'axios';
import Vue from 'vue'

Vue.use(VueSession);

export default {
  name: 'Login',
  components: { weatherdetails },
  data () {
    return {
      userid: '',
      pwd: '',
      userdata: '',
      loginError: false
    }
  },
  methods: {
    // To authenticate the user.
    authenticate: function(){
      for(var i=0; i<this.userdata.length; i++){
        var user = this.userdata[i];
        if(user.id == this.userid && user.password == this.pwd){
          this.loginError = false;
          this.$session.start();
          this.$session.set('uid', this.userid);
          this.$router.push({ name: 'weatherdetails', params: { userid: this.userid }});
          return;
        }
      }
      this.loginError = true;
      this.pwd = '';
    }
  },
  beforeCreate: function () {
    //Handling browser buttons.
    if (this.$session.exists()) {
      this.$router.push({ name: 'weatherdetails', params: { userid: this.$session.get('uid') }});
      return;
    }
    // Get user json data
    axios.get('static/User.json')
      .then((res) => {
        this.userdata = res.data;
      })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->

<style scoped>

.form-signin {
  max-width: 330px;
  padding: 15px;
  margin: 0 auto;
}
.form-signin .form-signin-heading,
.form-signin .checkbox {
  margin-bottom: 10px;
}
.form-signin .checkbox {
  font-weight: normal;
}
.form-signin .form-control {
  position: relative;
  height: auto;
  -webkit-box-sizing: border-box;
     -moz-box-sizing: border-box;
          box-sizing: border-box;
  padding: 10px;
  font-size: 16px;
}
.form-signin .form-control:focus {
  z-index: 2;
}
.form-signin input[type="email"] {
  margin-bottom: -1px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}
.form-signin input[type="password"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
</style>
