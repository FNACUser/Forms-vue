import Vue from 'vue';
import { markRaw } from 'vue';
import App from './App.vue';
import router from './router';
import axios from 'axios';
import Vuetify from 'vuetify';
import 'vuetify/dist/vuetify.min.css';
import pinia from "@/store/createPinia";
import {i18n} from './i18n';
import VueAlertify from 'vue-alertify';
import Vue2Filters from 'vue2-filters'
//import VueParticles from 'vue-particles';

import VuetifyMoney from "./components/vuetify-money";

var Vue2FiltersConfig = {
    
    percent: {
        decimalDigits: 0
    },
    currency: {
        symbol: '$',
        decimalDigits: 0,
        thousandsSeparator: '.',
        decimalSeparator: ',',
        symbolOnLeft: true,
        spaceBetweenAmountAndSymbol: true,
        showPlusSign: false

    }
}


Vue.use(Vue2Filters, Vue2FiltersConfig)
//Vue.use(VueParticles)
Vue.use(VueAlertify);
Vue.use(Vuetify);
Vue.use(VuetifyMoney);

pinia.use(({ store }) => { store.router = markRaw(router) });

Vue.config.productionTip = false;
Vue.prototype.$axios = axios;
window.axios = require('axios');
window.axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
window.axios.interceptors.request.use(
   config => {
       //const token = localStorageService.getAccessToken();
       const token =localStorage.getItem('access_token');
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



new Vue({
    
        vuetify:new Vuetify({
            theme: { dark: false },
            lang: {
                t: (key, ...params) => i18n.t(key, params),
              },

            }),
        pinia,
        i18n,
        router,
        render: h => h(App),

    }).$mount('#app')