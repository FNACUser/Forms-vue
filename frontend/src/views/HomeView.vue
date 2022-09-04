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
            @click:clear="clearVariables"
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
            @change="getQuestions"

            @click:clear="clearVariables"
            
          ></v-select>
      </v-col>
      </v-row>
      <v-row> 
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
  
      <v-col
       class="d-flex justify-space-around mb-6 align-end"
        cols="3"
      >
        <v-autocomplete
          v-model="selected_colleagues"
          :items="filteredEmployees"
          item-text="username"
          item-value="id"
          clearable
          label="Empleado"
          persistent-hint
          dense
          deletable-chips
          chips
          multiple
          return-object
          @change="sortSelectedColleagues"
         
        ></v-autocomplete>
      </v-col>
      
    </v-row>

    <v-row>

      <v-col
          v-for="(item, i) in mainStore.questions"
          :key="i"
          cols="3"
        >
          <v-card
          
          >
            <div >
              

                <v-card-title
                  class="text-h5"
                 >Pregunta {{i+1}}</v-card-title>
                <v-card-title
                  
                  v-text="item.Question"
                ></v-card-title>

                <v-card-subtitle >

                  <v-list disabled>
                    <v-subheader>Posibles respuestas:</v-subheader>
                    <v-list-item-group
                    class="text-h8"
                    >
                      <div
                        v-for="(possanswer, j) in JSON.parse(item.question_possible_answers.Question_possible_answers)"
                        :key="j"
                      >
                        <v-list-item-content>
                          <v-list-item-title >
                            - {{possanswer['texto']}}
                          </v-list-item-title>
                        </v-list-item-content>
                      </div>
                    </v-list-item-group>
                  </v-list>
                  
                </v-card-subtitle>                
              
            </div>
          </v-card>
        </v-col>

        <v-col
         
          cols="12"
        >

        <v-data-table
          :headers="tableHeader"
          :items="selected_colleagues"
          :items-per-page="5"
          class="elevation-1"
        >
        <template v-slot:item="{ item }">


            <tr>

                <td class="text-xs-left">{{ item.username }}</td>
                <td class="text-xs-left">{{ item.organization_area.Organization_area }}</td>
                <template >
                    <td v-for="(question,index) in mainStore.questions" :key="index">
                      
                    <v-select
                        
                        :items="JSON.parse(question.question_possible_answers.Question_possible_answers)"
                        item-text="texto"
                        item-value="valor"
                        clearable
                        @change="setAnswersArray(value,item.id,question.id )"
                      >
                    
                    </v-select>

                    </td>
                    
                </template>
                <td>
                    

                    <v-tooltip bottom>
                        <template #activator="{ on }">
                            <v-icon
                                v-on="on"
                                small
                                @click="deleteColleague(item)"
                            >
                                mdi-delete
                            </v-icon>
                        </template>
                        <span>Borrar</span>
                    </v-tooltip>
                </td>
            </tr>

</template>
      
        </v-data-table>

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

        selected_colleagues:[],
        selected_cycle:null,
        selected_network:null,
        selected_area:null,
        selected_node_segment_category:null,
        selected_network_mode_theme:null,
        selected_answers:[],
       
        //interactingColleagues:[],

        defaultHeader:[
          {
            text: 'Nombre Colega',
            align: 'start',
            value: 'username',
          },
          { text: 'Area', value: 'organization_area.Organization_area' },
          
          { text: 'Acciones'},
        ],



      }
    },
   

    computed:{

      filteredCycles(){
        return this.mainStore.cycles.filter(item=> item.Is_active); 
      },

      filteredEmployees(){

        //console.log(this.selected_area);

        if(this.selected_area){

          return this.mainStore.employees.filter(item=> item.id_organization_area===this.selected_area); 

        }
        else return null;
        
      },

      filteredNetwokModeThemes(){

        if(this.selected_network){

          let filteredArr = this.mainStore.network_modes.filter(item =>  item.id_network===this.selected_network && item.network_mode_theme);
          
          if (filteredArr && filteredArr.length){
            return filteredArr.map(item=> {
              return item.network_mode_theme;
              
              });
          }
          else return null;
        }
        else 
        return null;

      },

      tableHeader() {
            return this.makeTableHeader(this.mainStore.questions, this.defaultHeader, 'Pregunta');

        },
    

      ...mapStores(useMainStore),

    },

    methods:{

      setAnswersArray(value,employee_id,question_id){

        console.log(value);
        console.log(employee_id);
        console.log(question_id);

      },



      makeTableHeader(val, defaultHeader, text) {

            let headers = Object.assign([], defaultHeader);
            //console.log('entro a makeTableheader');

            if (val && val.length > 0) {
              console.log(val.length);
                //headers.splice(2, 1);
                val.forEach((question, index) => {
                    headers.splice(2 + index, 0, {
                        text: `${text} ${index + 1}`,
                        align: 'center',
                        sortable: false,
                    });
                });
            }

            return headers.reduce((acc, val) => acc.concat(val), []); //flattened the array
        },

      sortSelectedColleagues(){
        this.selected_colleagues.sort((a,b) => 
          (a.username.toLowerCase() < b.username.toLowerCase()) ? -1 : ((b.username.toLowerCase() > a.username.toLowerCase()) ? 1 : 0));

      },

      deleteColleague(item) {
           // this.item_index = this.items.indexOf(item)
            let item_index = this.selected_colleagues.findIndex(object => {
                return object.id==item.id});

            this.selected_colleagues.splice(item_index,1);
            
      },


      resetSelectedVariables(){

          this.selected_area=null;
          this.selected_cycle=null;
          this.selected_colleagues=null;
          this.selected_network=null;
          this.selected_node_segment_category=null;
          this.selected_network_mode_theme=null;
          this.mainStore.questions=[];


        },


        clearVariables(){

          this.mainStore.questions=[];

        },


        // setInteractingColleagues(){

        //   if(this.selected_employees){

        //     this.interactingColleagues=[...this.selected_employees];

        //   }

        // },

       async getQuestions(){
        if(this.selected_network && this.selected_network_mode_theme){

          let network_mode = this.mainStore.network_modes.filter(item =>  item.id_network===this.selected_network && item.id_network_mode_theme===this.selected_network_mode_theme)[0];
          //console.log(network_mode);
          this.mainStore.getNetworkModeQuestions(network_mode.id_network_mode)
         //console.log(this.mainStore.questions);
        }
        
       } 
    }
  }
</script>

