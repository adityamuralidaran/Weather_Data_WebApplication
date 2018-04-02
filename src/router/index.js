import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import weatherdetails from '@/components/weatherdetails'
import filterdetails from '@/components/filterdetails'

Vue.use(Router)


export default new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login,
      props: true
    },
    {
      path: '/weatherdetails/:userid',
      name: 'weatherdetails',
      component: weatherdetails,
      props: true
    },
    {
      path: '/filterdetails/:userid',
      name: 'filterdetails',
      component: filterdetails,
      props: true
    }
  ]
})
