<template>
  <v-container fill-height fluid>
      <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <v-card class="elevation-12">
              <v-img
                height="250px"
                src="images/OA-HUB-cropped.png"
              >
              <v-app-bar
                flat
                color="rgba(0, 0, 0, 0)"
              >
              
              </v-app-bar>
              </v-img>
              <v-card-text>
                <v-form v-model="valid_form">
                  
                  <v-text-field
                  prepend-icon ="mdi-email"
                  v-model="email"
                  label="Email"
                  type="text"
                  :rules="[v => !!v || $t('login.email_required'),
                            v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || $t('login.email_not_valid')]">
                  </v-text-field>

                  <v-text-field
                      @keyup.enter="logIn"
                      id="password"
                      prepend-icon ="mdi-lock"
                      v-model="password"
                      :label="$t('login.password')"
                      :type="show ? 'text' : 'password'"
                      :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                      @click:append="show = !show"
                      :rules="[v => !!v || $t('login.pwd_required'),
                              v => /^\w(?=.{4,})/.test(v) || $t('login.min_pwd')]"
                    >
                    </v-text-field>

                    <router-link to="forgot-password">{{$t('login.forgot_pwd')}}</router-link>

                  
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click='logIn' :disabled="!valid_form" >Login</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
      </v-layout>
  </v-container>
    

</template>

<script>

import { useMainStore } from '@/store/main'
import { mapStores} from 'pinia'

  export default {
    data(){
      return {
        email:null,
        password:null,
        show:false,
        // forgotURL: window.location.origin+"/forgot-password",
        valid_form:false
      }
    },

    computed:{

      ...mapStores(useMainStore),
    },


    methods: {

     async logIn(){

        let creds = {email:this.email,password:this.password};

        this.mainStore.logIn(creds);
    
     }


    }
}
</script>
