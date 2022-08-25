import { defineStore } from 'pinia'
import axios from 'axios'


export const useMainStore = defineStore('main', {
  state: () => {
    return { 
        count: 6,
        isLoggedIn : false,
        token:''

    }
  },
  // could also be defined as
  // state: () => ({ count: 0 })
  actions: {
    increment() {
      this.count++
    },

    async logIn(credentials){

  
        axios.post('http://localhost:5000/api/v1/login', credentials)
                  .then(response => {
                     
                      let accessToken = response.data.token;
                      localStorage.setItem('access_token', accessToken);
                      this.isLoggedIn=true;
                      this.router.push('/home').catch((e) => {console.log(e)});
                      
                  })
                 .catch( error => {
                      console.log(error);
                      localStorage.removeItem('access_token');
                      this.isLoggedIn=false;
                      this.router.push('/login').catch(() => {});
  
                 });
          
       },

    logout(){

        localStorage.removeItem('access_token');
        this.isLoggedIn=false;
        this.router.push('/login')
  


    }
  },
})