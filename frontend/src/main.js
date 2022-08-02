import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios from 'axios'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { loadFonts } from './plugins/webfontloader'

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

loadFonts()

//import './assets/main.css'

const vuetify = createVuetify({
  components,
  directives,
})

const axiosInstance = axios.create({
   // withCredentials: true,
  })

const app = createApp(App)

app.config.globalProperties.$axios = { ...axiosInstance }

app.use(createPinia())
app.use(router)
app.use(vuetify)

app.mount('#app')
