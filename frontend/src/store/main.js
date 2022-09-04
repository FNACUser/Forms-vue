import { defineStore } from 'pinia'
import axios from 'axios'
import jwt_decode from "jwt-decode";


export const useMainStore = defineStore('main', {
  state: () => {
    return { 
        count: 6,
        // isLoggedIn : false,
        token: localStorage.getItem('access_token') || '',
        user:{
          name:'',
          email:'',
          role:''
        },
        employees:[],
        //users: [],
        cycles: [],
        networks:[],
        areas:[],
        network_modes:[],
        questions:[]

    }
  },

  getters: {
    isLoggedIn: state => !!state.token,
  },
  // could also be defined as
  // state: () => ({ count: 0 })
  actions: {
    increment() {
      this.count++
    },

    async initialize(){

      console.log('ENV BACKEND_URL='+ process.env.VUE_APP_BACKEND_URL);
      this.getAreas();
      this.getEmployees();
      this.getNetworks();
      this.getCycles();
      
    },

    async logIn(credentials){

  
        axios.post(process.env.VUE_APP_BACKEND_URL+'login', credentials)
                  .then(response => {
                     
                      let accessToken = response.data.token;
                      localStorage.setItem('access_token', accessToken);
                      this.token = accessToken
                      
                      let token_decoded = jwt_decode(accessToken);
                      this.setLoggedUser(token_decoded);

                     
                     // this.isLoggedIn=true;
                      this.initialize();
                      this.router.push('/home').catch((e) => {console.log(e)});
                      
                  })
                 .catch( error => {
                      console.log(error);
                      localStorage.removeItem('access_token');
                      //this.isLoggedIn=false;
                      this.router.push('/login').catch(() => {});
  
                 });
          
       },

    logout(){

        localStorage.removeItem('access_token');
        this.user={
          name:'',
          email:'',
          role:''
        };
        this.token='';
       // this.isLoggedIn=false;
       this.router.push('/login').catch(() => {});
  
    },

    setLoggedUser(token){

      this.user.name=token.username;
      this.user.email=token.email;
      this.user.role=token.roles[0].name;

    },


    async getNetworkModes(selected_cycle){

      console.log('ingresó a getNetworkModes');

      if(selected_cycle){
         const resp = await axios.get(process.env.VUE_APP_BACKEND_URL+'cycle/'+selected_cycle +'/network_modes');
        // console.log(resp.data);
         this.network_modes=resp.data;
      }   

   },


   async getNetworkModeQuestions(selected_network_mode){

    console.log('ingresó a ggetNetworkModeQuestions');

    if(selected_network_mode){
       const resp = await axios.get(process.env.VUE_APP_BACKEND_URL+'network_mode/'+selected_network_mode +'/questions');
       console.log(resp.data);
       this.questions=resp.data;
    }   

 },

   async getEmployees(){

     const employees = await axios.get(process.env.VUE_APP_BACKEND_URL+'users');
     this.employees = employees.data;

   },

   async getCycles(){

     const cycles = await axios.get(process.env.VUE_APP_BACKEND_URL+'cycles');
     this.cycles = cycles.data;

   },

   async getNetworks(){

     const networks = await axios.get(process.env.VUE_APP_BACKEND_URL+'networks');
     this.networks = networks.data;

   },

   async getAreas(){

     const areas = await axios.get(process.env.VUE_APP_BACKEND_URL+'areas');
     this.areas = areas.data;

   },

  },
})