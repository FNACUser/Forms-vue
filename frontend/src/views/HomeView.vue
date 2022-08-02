
<template>
  <v-container>
    <v-row>
      <v-col
        class="d-flex"
        cols="4"
        sm="4"
      >
        <v-autocomplete
          v-model="selected_user"
          :items="users"
          item-title="username"
          item-value="id"
          clearable
          hint="Usuarios"
          persistent-hint
          dense
        ></v-autocomplete>
      </v-col>

      <v-col
        class="d-flex"
        cols="3"
        sm="3"
      >
        <v-select
          v-model="selected_cycle"
          :items="filteredCycles"
          label="Periodos"
          item-title="Cycle"
          item-value="id_cycle"
          clearable
          @change="getNetworkModes"
        ></v-select>
      </v-col>

       <v-col
        class="d-flex"
        cols="3"
        sm="3"
        >
          <v-select
            v-model="selected_network"
            :items="networks"
            label="Tipo de Cuestionario"
            item-title="name"
            item-value="id"
            clearable
          ></v-select>
      </v-col>
    </v-row>
    <v-row>
      <v-col
        class="d-flex"
        cols="4"
        sm="4"
        >
          <v-select
            v-model="selected_area"
            :items="areas"
            label="Areas"
            item-title="Organization_area"
            item-value="id_organization_area"
            clearable
          ></v-select>
      </v-col>


    </v-row>

{{selected_user}}
{{selected_area}}
{{selected_cycle}}
{{selected_network}}
  </v-container>

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
    
      // filteredNetworkModes(){
      //   return this.networkmodes.filter((item, index) => {
      //               const _value = item.Network_mode;
      //               return index === this.networkmodes.findIndex(obj => {
      //                 return obj.Network_mode === _value;
      //               });
      //             });

      // }
    },

    methods:{

      async initialize(){

        const users = await this.$axios.get('http://localhost:5000/api/v1/users');
        this.users = users.data;
        const cycles = await this.$axios.get('http://localhost:5000/api/v1/cycles');
        this.cycles = cycles.data;
        const networks = await this.$axios.get('http://localhost:5000/api/v1/networks');
        this.networks = networks.data;
        const areas = await this.$axios.get('http://localhost:5000/api/v1/areas');
        this.areas = areas.data;

      },


      async getNetworkModes(){

         console.log('ingresó a getNetworkModes');

         const resp = this.$axios.get('http://localhost:5000/api/v1/cycle/'+this.selected_cycle +'/network_modes');

         console.log(resp);

      }
    }
  }
</script>

