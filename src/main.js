// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Vue2Filters from 'vue2-filters'
Vue.use(Vue2Filters)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  router,
  template: `
  <div id="app" class="haze">
    <nav class="navbar navbar-inverse">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <p class="navbar-brand" >Weather Application</p>
        </div>
      </div>
    </nav>

    <router-view></router-view>
  </div>
</div>
  `
}).$mount('#app')
