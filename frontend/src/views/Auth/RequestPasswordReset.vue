<template>
  
  <v-container fill-height fluid>
         <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <v-card class="elevation-12">
              <v-toolbar dark color="primary">
                <v-toolbar-title>{{$t('login.reset_password.title')}}</v-toolbar-title>
                <v-spacer></v-spacer>
              </v-toolbar>
              <v-card-text>
                <v-form v-model="valid_form">
                   <v-text-field
                    prepend-icon="mdi-email"
                    v-model="email"
                    label="Email"
                    type="text"
                    :rules="[v => !!v || $t('login.email_required'),
                             v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || $t('login.email_not_valid')]">
                    </v-text-field>                
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn  @click='cancel' :disabled="sending_email">{{$t('menus.cancel')}}</v-btn>
                <v-btn color="primary" @click='requestPasswordReset' :disabled="isValidForm">{{$t('login.reset_password.send_request')}}</v-btn>
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
        email: null,
        has_error: false,
        valid_form:false,
        sending_email:false
      }
    },

    computed:{

      isValidForm(){
          return (!this.valid_form  || this.sending_email);
        },

    },
    methods: {

      ...mapActions(useMainStore, ['setFlashMessage']),



      cancel(){

        this.$router.push({ path: 'Login' });
        //this.$router.replace({ path: 'Login' });

      },

        requestPasswordReset() {

          this.sending_email=true;

            this.$axios.post(process.env.VUE_APP_BACKEND_URL+"/request_password_reset", {email: this.email,lang:this.$i18n.locale})
            .then(response => { 
               // console.log(response);
                this.sending_email=false;
                this.setFlashMessage({message:response.data , type:'success'});
                this.$router.replace("/");
               
            })
            .catch(error => {

                //console.log(error);
                this.sending_email=false;
                this.setFlashMessage({message:error.response.data, type:'error'});
                this.email="";
            });
        }
    }
}
</script>
