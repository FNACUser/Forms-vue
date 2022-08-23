<template>
 
    <div >

      <br/>
      <br/>

      <v-row class="back-top"></v-row>

       <v-container fluid >
       <v-row>
         <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <v-card class="elevation-12">
              <v-toolbar dark color="primary">
                <v-toolbar-title>Login...</v-toolbar-title>
                <v-spacer></v-spacer>

              </v-toolbar>
              <v-card-text>
                <v-form>
                   <v-text-field
                    prepend-icon ="mdi-email"
                    v-model="email"
                    label="Email"
                    type="text"
                    :rules="[v => !!v || 'E-mail es requerido!',
                             v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'E-mail no es válido']">
                    </v-text-field>
                  <v-text-field
                      @keyup.enter="logIn"
                      id="password"
                      prepend-icon ="mdi-lock"
                      v-model="password"
                      label="Contraseña"
                      :type="show ? 'text' : 'password'"
                      :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                      @click:append="show = !show"
                      :rules="[v => !!v || 'Contraseña es requerida!',
                              v => /^\w(?=.{4,})/.test(v) || 'Contraseña debe ser mínimo de 5 caracteres!']"
                    >
                    </v-text-field>

                    <a :href="forgotURL">¿Olvidó su contraseña?</a>

                  
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click='logIn'>Login</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
       </v-row>

      </v-container>
    </div>

  

</template>

<script>

 

  export default {
    data(){
      return {
        email:null,
        password:null,
        show:false,
        forgotURL: window.location.origin+"/#/forgot-password"
      }
    },


    methods: {

    async logIn(){

      let creds = {email:this.email,password:this.password};

      this.$axios.post('http://localhost:5000/api/v1/login', creds)
                .then(response => {

                    let accessToken = response.data.token;
                    localStorage.setItem('access_token', accessToken);
                    this.$router.push('/');

                })
               .catch( error => {
                    console.log(error.response.data.message);
                    localStorage.removeItem('access_token');
                    this.$router.push('/login')

               });
        
     }


    }
}
</script>
