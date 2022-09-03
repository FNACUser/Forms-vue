import { defineStore } from 'pinia'
import axios from 'axios'
import jwt_decode from "jwt-decode";


export const useMainStore = defineStore('main', {
  state: () => {
    return { 
        count: 6,
        isLoggedIn : false,
        token:'',
        user:{
          name:'',
          email:''
        },
        employees:[],
        users: [],
        cycles: [],
        networks:[],
        areas:[],
        network_modes:[]

    }
  },
  // could also be defined as
  // state: () => ({ count: 0 })
  actions: {
    increment() {
      this.count++
    },

    async initialize(){

      //console.log('ENV BACKEND_URL='+ process.env.BACKEND_URL);
      this.getAreas();
      this.getUsers();
      this.getNetworks();
      this.getCycles();
      
    },

    async logIn(credentials){

  
        axios.post(process.env.BACKEND_URL+'login', credentials)
                  .then(response => {
                     
                      let accessToken = response.data.token;
                      let token_decoded = jwt_decode(accessToken);
                      console.log(token_decoded);
                      this.user.name=token_decoded.username;
                      this.user.email=token_decoded.email;

                      localStorage.setItem('access_token', accessToken);
                      this.isLoggedIn=true;
                      this.initialize();
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
  
    },

    async getNetworkModes(selected_cycle){

      console.log('ingresó a getNetworkModes');

      if(selected_cycle){
         const resp = await axios.get(process.env.BACKEND_URL+'cycle/'+selected_cycle +'/network_modes');
         console.log(resp.data);
         this.network_modes=resp.data;
      }   

   },

   async getUsers(){

     const users = await axios.get(process.env.BACKEND_URL+'users');
     this.users = users.data;

   },

   async getCycles(){

     const cycles = await axios.get(process.env.BACKEND_URL+'cycles');
     this.cycles = cycles.data;

   },

   async getNetworks(){

     const networks = await axios.get(process.env.BACKEND_URL+'networks');
     this.networks = networks.data;

   },

   async getAreas(){

     const areas = await axios.get(process.env.BACKEND_URL+'areas');
     this.areas = areas.data;

   },

  },
})