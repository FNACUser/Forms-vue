import Vue from 'vue'
import { markRaw } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import pinia from "@/store/createPinia";
import VueI18n from 'vue-i18n'

Vue.use(VueI18n)
Vue.use(Vuetify)

pinia.use(({ store }) => { store.router = markRaw(router) })

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


   /**
 * Next we will register the CSRF Token as a common header with Axios so that
 * all outgoing HTTP requests automatically have it attached. This is just
 * a simple convenience so we don't have to attach every token manually.
 */

// let token = document.head.querySelector('meta[name="csrf-token"]');

// if (token) {
//     window.axios.defaults.headers.common['X-CSRF-TOKEN'] = token.content;
// } else {
//     console.error('CSRF token not found!!');
// }


// Ready translated locale messages
const messages = {
  en: {
    message: {
      hello: 'hello world'
    }
  },
  es: {
    message: {
      hello: 'Hola mundo'
    }
  }
}


// Create VueI18n instance with options
const i18n = new VueI18n({
  locale: 'es', // set locale
  messages, // set locale messages
})

new Vue({
  render: h => h(App),
  vuetify:new Vuetify({
    theme: { dark: false },

  }),
  pinia,
  router,
  i18n


}).$mount('#app')