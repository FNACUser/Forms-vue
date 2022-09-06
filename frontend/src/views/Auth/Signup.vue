<template>
  <v-app id="inspire">
    <v-main>

      <v-row class="back-top"></v-row>  
      <v-container fluid >
        <v-row>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <v-card class="elevation-12">
              <v-toolbar dark color="primary">
                <v-toolbar-title>Registrarse...</v-toolbar-title>
                <v-spacer></v-spacer>
              </v-toolbar>
              <v-card-text>

                <v-form>
                  <v-text-field prepend-icon="person" v-model="name" label="Usuario" type="text"></v-text-field>
                  <v-text-field prepend-icon="email" v-model="email" label="Email" type="text"
                  :rules="[v => !!v || 'E-mail es requerido!',
                             v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'E-mail no es válido']"
                  ></v-text-field>
                  <v-text-field id="password" prepend-icon="lock" v-model="password" label="Password" 
                    :type="show ? 'text' : 'password'"
                    :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                    @click:append="show = !show"
                    :rules="[v => !!v || 'Contraseña es requerida!',
                             v => /^\w(?=.{4,})/.test(v) || 'Contraseña debe ser mínimo de 5 caracteres!']"
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" type="submit" @click="registerUser">Registrarse</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
 
  import {mapGetters}  from 'vuex'
  export default {
    
      data(){
          return {
            name: null,
            email: null,
            password:null,
            show:false

        }
      },
      computed: {
     ...mapGetters(["getToken"])
     },
      methods:{

          async registerUser(){
          
             await this.$store.dispatch('register', {
              name:this.name,
              email:this.email,
              password:this.password});
             if(this.getToken) {
                this.$axios.defaults.headers.common['Authorization'] = "Bearer " + this.getToken;
                this.$store.dispatch('initializeStore')
              }  

            
          }


      }
  
    
}
</script>