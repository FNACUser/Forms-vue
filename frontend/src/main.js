import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'

Vue.use(Vuetify)

Vue.config.productionTip = false

Vue.prototype.$axios = axios;

window.axios = require('axios');

window.axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';

window.axios.interceptors.request.use(
   config => {
       //const token = localStorageService.getAccessToken();
       const token =localStorage.getItem('access_token');
       //console.log(token)
       if (token) {
          //config.headers['Authorization'] = 'Bearer ' + token;
           config.headers['x-access-token'] =  token;
       }
       // config.headers['Content-Type'] = 'application/json';
       return config;
   },
   error => {
       Promise.reject(error)
   });

new Vue({
  render: h => h(App),
  vuetify:new Vuetify({
    theme: { dark: false },

  }),
  router
}).$mount('#app')