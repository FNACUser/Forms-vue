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
          @change="mainStore.getNetworkModes(selected_cycle)"
          @click:clear="resetSelectedVariables"
        ></v-select>
      </v-col>

       <v-col
        cols="3"
         class="d-flex justify-space-around mb-6 align-end"
        >
          <v-select
            v-model="selected_network"
            :items="mainStore.networks"
            label="Tipo de Cuestionario"
            item-text="name"
            item-value="id"
            clearable
          ></v-select>
      </v-col>

      <v-col
        cols="3"
         class="d-flex justify-space-around mb-6 align-end"
         v-if="filteredNetwokModeThemes"
        >
          <v-select
            v-model="selected_network_mode_theme"
            :items="filteredNetwokModeThemes"
            label="Temáticas de las preguntas"
            item-text="Network_mode_theme"
            item-value="id_network_mode_theme"
            clearable
            
          ></v-select>
      </v-col>
      <v-col
        cols="3"
        class="d-flex justify-space-around mb-6 align-end"
        >
          <v-select
            v-model="selected_area"
            :items="mainStore.areas"
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
          :items="mainStore.users"
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

import { useMainStore } from '@/store/main'
import { mapStores} from 'pinia'


  export default {
    data() {
      return {

        selected_user:null,
        selected_cycle:null,
        selected_network:null,
        selected_area:null,
        selected_node_segment_category:null,
        selected_network_mode_theme:null
      }
    },
   

    computed:{

      filteredCycles(){
        return this.mainStore.cycles.filter(item=> item.Is_active); 
      },

      filteredNetwokModeThemes(){

        //console.log(this.selected_network);

        return this.mainStore.network_modes.map(item=> {
         if (item.id_network===this.selected_network){
          console.log('son iguales');
          return item.network_mode_theme;
         }
          
        });

      },
    

      ...mapStores(useMainStore),

    },

    methods:{


      resetSelectedVariables(){

          this.selected_area=null;
          this.selected_cycle=null;
          this.selected_user=null;
          this.selected_network=null;
          this.selected_node_segment_category=null;
          this.selected_network_mode_theme=null;


        }
    }
  }
</script>

