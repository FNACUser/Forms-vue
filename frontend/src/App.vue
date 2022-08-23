<template>

    <v-app>
      <v-navigation-drawer 
        v-model="drawer"
        :clipped="$vuetify.breakpoint.lgAndUp"
        app
      >
       
      </v-navigation-drawer>
      <v-app-bar 
        :clipped-left="$vuetify.breakpoint.lgAndUp"
        app
      >

        <v-app-bar-nav-icon @click.stop="drawer = !drawer"/>

      </v-app-bar>

        <header>
          <link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900" rel="stylesheet">
          <link href="https://cdn.jsdelivr.net/npm/@mdi/font@6.x/css/materialdesignicons.min.css" rel="stylesheet">
          
        </header>
        <v-main>
          <v-container fluid>
              <router-view ></router-view>
          </v-container>
        </v-main>

        <v-footer app>
          
        </v-footer>

         </v-app>
</template>

<script>

 export default{

  data(){
    return {

      drawer: true,

    }

  }


 }

</script>

<style>

</style>

