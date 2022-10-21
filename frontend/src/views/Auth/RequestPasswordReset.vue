<template>
  <v-app id="inspire">
    <v-main >
      <v-row class="back-top"></v-row>
       <v-container fluid >
       <v-row>
         <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <v-card class="elevation-12">
              <v-toolbar dark color="primary">
                <v-toolbar-title>Restablecer contraseña...</v-toolbar-title>
                <v-spacer></v-spacer>
              </v-toolbar>
              <v-card-text>
                <v-form v-model="valid_form">
                   <v-text-field
                    prepend-icon="mdi-email"
                    v-model="email"
                    label="Email"
                    type="text"
                    :rules="[v => !!v || 'E-mail es requerido!',
                             v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'E-mail no es válido']">
                    </v-text-field>                
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click='cancel' >Cancelar</v-btn>
                <v-btn color="primary" @click='requestResetPassword' :disabled="isValidForm">Enviar solicitud</v-btn>
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
        email: null,
        has_error: false,
        valid_form:false
      }
    },

    computed:{

      isValidForm(){
          return !this.valid_form ;
        },

    },
    methods: {


      //  ...mapMutations([
      //       'setFlashMessage'
      //   ]),

      cancel(){

        this.$router.push({ path: 'Login' });
        //this.$router.replace({ path: 'Login' });

      },

        requestResetPassword() {

        
            this.$axios.post("api/forgot-password", {email: this.email})
            .then(response => { 
              console.log(response)
                this.setFlashMessage({message:'Un correo ha sido enviado a su cuenta para restablecer su contraseña: ' +this.email, type:'success'});
                this.$router.replace("/");
            })
            .catch(error => {

                console.log(error)

                this.setFlashMessage({message:'No existe la dirección de correo: ' +this.email, type:'error'});
                this.email="";
            });
        }
    }
}
</script>