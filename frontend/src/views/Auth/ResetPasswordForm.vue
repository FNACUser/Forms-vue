<template>
      <v-container fill-height fluid>
         <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <v-card class="elevation-12">
              <v-toolbar dark color="primary">
                <v-toolbar-title>{{$t('login.reset_password.change_pwd')}}</v-toolbar-title>
                <v-spacer></v-spacer>
              </v-toolbar>
              <v-card-text>

                <v-form v-model="valid_form">
                 
                  <v-text-field prepend-icon="mdi-email" v-model="email" label="Email" type="text" disabled
                  :rules="[v => !!v || 'E-mail es requerido!',
                             v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'E-mail no es válido']"
                  ></v-text-field>
                  <v-text-field id="password" prepend-icon="mdi-lock" v-model="password" :label="$t('login.new_password')" 
                    :type="show_pwd ? 'text' : 'password'"
                    :append-icon="show_pwd ? 'mdi-eye' : 'mdi-eye-off'"
                    @click:append="show_pwd = !show_pwd"
                    :rules="[v => !!v || $t('login.pwd_required'),
                              v => /^\w(?=.{4,})/.test(v) || $t('login.min_pwd')]"
                  ></v-text-field>
                  <v-text-field id="confirmation_password" prepend-icon="mdi-lock" v-model="confirmation_password" :label="$t('login.confirmation_password')" 
                    :type="show_conf_pwd ? 'text' : 'password'"
                    :append-icon="show_conf_pwd ? 'mdi-eye' : 'mdi-eye-off'"
                    @click:append="show_conf_pwd = !show_conf_pwd"
                    :rules="[v => !!v || $t('login.pwd_required'),
                              v => /^\w(?=.{4,})/.test(v) || $t('login.min_pwd'),
                              v => v === this.password || $t('login.confirmation_pwd_not_match') ]"
                             
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn  @click='cancel' >{{$t('menus.cancel')}}</v-btn>
                <v-btn color="primary" type="submit" @click="resetPassword" :disabled="!valid_form">{{$t('login.reset_password.change_pwd')}}</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
</template>

<script>

import { useMainStore } from '@/store/main'
import { mapActions} from 'pinia'

export default {
    data() {
      return {
        token: null,
        email: this.$route.params.email,
        password: null,
        confirmation_password: null,
        has_error: false,
        show_pwd:false,
        show_conf_pwd:false,
        valid_form:false
      }
    },
    methods: {

      ...mapActions(useMainStore, ['setFlashMessage']),

      
      cancel(){

        this.$router.replace('/');

       },

        resetPassword() {

          this.$axios.post(process.env.VUE_APP_BACKEND_URL+"/reset_password", 
            {
                token: this.$route.params.token,
                email: this.$route.params.email,
                password: this.password,
                confirmation_password: this.confirmation_password
            })
            .then(response => {
               // console.log(response);
                this.setFlashMessage({message:response.data, type:'success'});
                this.$router.replace("/");
               
            })
            .catch(error => {

             // console.log(error.response);

              this.setFlashMessage({message:error.response.data, type:'error'});

          
            });
        }
    }
}
</script>