<template>
    <v-menu
          bottom
          left>
            <template v-slot:activator="{ on, attrs }">
              <v-btn 
                icon
                v-bind="attrs"
                v-on="on"
              >
                <v-icon>mdi-web</v-icon>{{$i18n.locale}}
              </v-btn>
            </template>
            <v-list>
              <v-list-item v-for="locale in filteredLocales" :key="locale">
                <v-list-item-title @click="switchLocale(locale)">{{locale.toUpperCase()}}</v-list-item-title>
              </v-list-item>
            
            </v-list>
        </v-menu>

</template>
<script>

export default {
  name: 'LocaleSwitcher',
  data(){
    return {
        locales: process.env.VUE_APP_I18N_SUPPORTED_LOCALES.split(',')
    }

  },
  computed: {

    filteredLocales(){

      return this.locales.filter(item => item !== this.$i18n.locale);


    }
    
  },
  methods: {
    switchLocale(locale) {

      if (this.$i18n.locale !== locale) {
            this.$i18n.locale = locale
      }
    }
  }
}

</script>