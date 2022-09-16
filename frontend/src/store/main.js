import { defineStore } from 'pinia'
import axios from 'axios'
import jwt_decode from "jwt-decode";
import {i18n} from '../i18n'

const null_user={
  id:'',
  name:'',
  email:'',
  role:''
};

export const useMainStore = defineStore('main', {
  state: () => {
    return { 
        
        token: localStorage.getItem('access_token') || '',    
        logged_user:null_user,
        employees:[],
        cycles: [],
        networks:[],
        areas:[],
        network_modes:[],
        loader: false
        // questions:[]

    }
  },

  getters: {
    isLoggedIn: state => !!state.token,
  },
  // could also be defined as
  // state: () => ({ count: 0 })
  actions: {
    

    async initialize(){

      console.log('ENV BACKEND_URL='+ process.env.VUE_APP_BACKEND_URL);
      this.getAreas();
      this.getEmployees();
      this.getNetworks();
      this.getCycles();
      
    },

    async logIn(credentials){

  
        axios.post(process.env.VUE_APP_BACKEND_URL+'/login', credentials)
                  .then(response => {
                     
                      let accessToken = response.data.token;
                      localStorage.setItem('access_token', accessToken);
                      this.token = accessToken;
                      this.setLoggedUser();
                      this.initialize();
                      this.router.push('/home').catch((e) => {console.log(e)});
                      
                  })
                 .catch( error => {
                      console.log(error);
                      this.$reset();
                      localStorage.removeItem('access_token');
                      this.router.push('/login').catch(() => {});
  
                 });
          
       },

    logout(){

        this.$reset();
        localStorage.removeItem('access_token');
        this.logged_user=null_user;
        this.token='';
       
       this.router.push('/login').catch(() => {});
  
    },


    setLoggedUser(){

      let decoded_token = jwt_decode(this.token);
      this.logged_user.id = decoded_token.id;
      this.logged_user.name=decoded_token.username;
      this.logged_user.email=decoded_token.email;
      this.logged_user.role=decoded_token.roles[0].name;

    },


    async getNetworkModes(selected_cycle){

      if(selected_cycle){
         const resp = await axios.get(process.env.VUE_APP_BACKEND_URL+'/cycle/'+selected_cycle +'/network_modes');
         this.network_modes=resp.data;
      }   

   },


   async getEmployees(){

     const employees = await axios.get(process.env.VUE_APP_BACKEND_URL+'/users');
     this.employees = employees.data;

   },

   async getCycles(){

     const cycles = await axios.get(process.env.VUE_APP_BACKEND_URL+'/cycles');
     this.cycles = cycles.data;

   },

   async getNetworks(){

     const networks = await axios.get(process.env.VUE_APP_BACKEND_URL+'/networks/'+i18n.locale);
     this.networks = networks.data;

   },

   async getAreas(){

     const areas = await axios.get(process.env.VUE_APP_BACKEND_URL+'/areas');
     this.areas = areas.data;

   },

   

  },
})