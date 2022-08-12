<template>
<div>
    <v-row >
      

      <v-col
        class="d-flex justify-space-around mb-6 align-end"
        cols="3"
      >
        <v-select
          v-model="selected_cycle"
          :items="filteredCycles"
          label="Periodo"
          item-text="Cycle"
          item-value="id_cycle"
          clearable
          @change="getNetworkModes"
          @click:clear="resetSelectedVariables"
        ></v-select>
      </v-col>

       <v-col
        cols="3"
         class="d-flex justify-space-around mb-6 align-end"
        >
          <v-select
            v-model="selected_network"
            :items="networks"
            label="Tipo de Cuestionario"
            item-text="name"
            item-value="id"
            clearable
          ></v-select>
      </v-col>
      <v-col
        cols="3"
        class="d-flex justify-space-around mb-6 align-end"
        >
          <v-select
            v-model="selected_area"
            :items="areas"
            label="Area"
            item-text="Organization_area"
            item-value="id_organization_area"
            clearable
          ></v-select>
      </v-col>
    </v-row>
    <v-row>

      <v-col
       class="d-flex justify-space-around mb-6 align-end"
        cols="3"
      >
        <v-autocomplete
          v-model="selected_user"
          :items="users"
          item-text="username"
          item-value="id"
          clearable
          label="Usuario"
          persistent-hint
          dense
        ></v-autocomplete>
      </v-col>
      
    </v-row>
</div>

</template>

<script>
  export default {
    data() {
      return {
        users: [],
        cycles: [],
        networks:[],
        areas:[],
        selected_user:null,
        selected_cycle:null,
        selected_network:null,
        selected_area:null,
      }
    },
    async mounted() {
      this.initialize();
    },

    computed:{

      filteredCycles(){
        return this.cycles.filter(item=> item.Is_active); 
      },
    

    },

    methods:{

      async initialize(){

        this.getAreas();
        this.getUsers();
        this.getNetworks();
        this.getCycles();
        

      },


      async getNetworkModes(){

         console.log('ingresó a getNetworkModes');

         if(this.selected_cycle){
            const resp = await this.$axios.get('http://localhost:5000/api/v1/cycle/'+this.selected_cycle +'/network_modes');
            console.log(resp.data);
         }   

      },

      async getUsers(){

        const users = await this.$axios.get('http://localhost:5000/api/v1/users');
        this.users = users.data;

      },

      async getCycles(){

        const cycles = await this.$axios.get('http://localhost:5000/api/v1/cycles');
        this.cycles = cycles.data;

      },

      async getNetworks(){

        const networks = await this.$axios.get('http://localhost:5000/api/v1/networks');
        this.networks = networks.data;

      },

      async getAreas(){

        const areas = await this.$axios.get('http://localhost:5000/api/v1/areas');
        this.areas = areas.data;

      },




      resetSelectedVariables(){

          this.selected_area=null;
          this.selected_cycle=null;
          this.selected_user=null;
          this.selected_network=null;


        }
    }
  }
</script>

