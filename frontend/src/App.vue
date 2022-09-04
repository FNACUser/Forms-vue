<template>

    <v-app>
      <v-navigation-drawer 
        v-model="drawer"
        :clipped="$vuetify.breakpoint.lgAndUp"
        v-if="mainStore.isLoggedIn"
        app
      >
       
      </v-navigation-drawer>
      <v-app-bar 
        :clipped-left="$vuetify.breakpoint.lgAndUp"
        v-if="mainStore.isLoggedIn"
        app
      >

        <v-app-bar-nav-icon @click.stop="drawer = !drawer" v-if="mainStore.isLoggedIn"/>
        <v-spacer></v-spacer>
        <v-toolbar-items v-if="mainStore.isLoggedIn">

                <v-btn text v-if="mainStore.isLoggedIn">{{ mainStore.user.name }}</v-btn>
                <v-btn icon>
                    <v-icon>mdi-web</v-icon>
                </v-btn>
                <v-btn icon @click="mainStore.logout" v-if="mainStore.isLoggedIn">
                    <v-icon>mdi-logout</v-icon>
                </v-btn>

            </v-toolbar-items>

      </v-app-bar>

        <header>
          <link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900" rel="stylesheet">
          <link href="https://cdn.jsdelivr.net/npm/@mdi/font@6.x/css/materialdesignicons.min.css" rel="stylesheet">
          
        </header>
        <v-main>
         
              <router-view ></router-view>
         
        </v-main>

        <v-footer app>
          
        </v-footer>

         </v-app>
</template>

<script>
 
 
 import { useMainStore } from '@/store/main'
 import { mapStores} from 'pinia'

 export default{

  data(){
      return {
        drawer: true,
      }
  },

  computed:{
    ...mapStores(useMainStore),
  },

  created() {

       
        if (this.mainStore.isLoggedIn) {
            //console.log('pasa por aki');
            this.mainStore.initialize();

        }
    },


 }

</script>

<style>

</style>

