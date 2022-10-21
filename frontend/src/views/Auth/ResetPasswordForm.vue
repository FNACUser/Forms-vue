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
                <v-toolbar-title>Reiniciar Contraseña...</v-toolbar-title>
                <v-spacer></v-spacer>
              </v-toolbar>
              <v-card-text>

                <v-form>
                 
                  <v-text-field prepend-icon="mdi-email" v-model="email" label="Email" type="text" disabled
                  :rules="[v => !!v || 'E-mail es requerido!',
                             v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'E-mail no es válido']"
                  ></v-text-field>
                  <v-text-field id="password" prepend-icon="mdi-lock" v-model="password" label="Contraseña" 
                    :type="show_pwd ? 'text' : 'password'"
                    :append-icon="show_pwd ? 'mdi-eye' : 'mdi-eye-off'"
                    @click:append="show_pwd = !show_pwd"
                    :rules="[v => !!v || 'Contraseña es requerida!',
                             v => /^\w(?=.{4,})/.test(v) || 'Contraseña debe ser mínimo de 5 caracteres!']"
                  ></v-text-field>
                  <v-text-field id="confirmation_password" prepend-icon="lock" v-model="password_confirmation" label="Confirmación de Contraseña" 
                    :type="show_conf_pwd ? 'text' : 'password'"
                    :append-icon="show_conf_pwd ? 'mdi-eye' : 'mdi-eye-off'"
                    @click:append="show_conf_pwd = !show_conf_pwd"
                    :rules="[v => !!v || 'Contraseña es requerida!',
                             v => /^\w(?=.{4,})/.test(v) || 'Contraseña debe ser mínimo de 5 caracteres!',
                             v => v=== this.password || 'La contraseña de confirmación no coincide!!']"
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click='cancel' >Cancelar</v-btn>
                <v-btn color="primary" type="submit" @click="resetPassword">Cambiar contraseña</v-btn>
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

//import {mapMutations} from 'vuex'

export default {
    data() {
      return {
        token: null,
        email: this.$route.params.email,
        password: null,
        password_confirmation: null,
        has_error: false,
        show_pwd:false,
        show_conf_pwd:false
      }
    },
    methods: {

      //  ...mapMutations([
      //       'setFlashMessage'
      //   ]),

      cancel(){

        this.$router.replace('/');

       },

        resetPassword() {

          this.$axios.post("api/reset-password", {
                token: this.$route.params.token,
                email: this.$route.params.email,
                password: this.password,
                password_confirmation: this.password_confirmation
            })
            .then(response => {
                console.log(response);
                this.$store.dispatch('login', {
                  email:this.$route.params.email,
                  password:this.password
                  });
               
            })
            .catch(error => {

              console.log(error.response);

              this.setFlashMessage({message:error.response.data.message, type:'error'});

                //console.error(error);
            });
        }
    }
}
</script>