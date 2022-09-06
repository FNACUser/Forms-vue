<template>
  <v-container  fluid>
    <v-row dense>
      <v-col
        class="d-flex justify-space-around mb-6 align-end"
        cols="3"
      >
        <v-select
          v-model="selected_cycle"
          :items="filteredCycles"
          :label="$t('period')"
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
            return-object
            @click:clear="clearVariables"
            @change="getQuestions"
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
      <v-row v-if="selected_network && selected_network.name==='Actor'"> 
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
          small-chips
          multiple
          return-object
          @change="sortSelectedColleagues"
         
        ></v-autocomplete>
      </v-col>
      
    </v-row>

    <v-row dense justify="space-around">

      <v-col cols="3">

        <div v-for="(item, i) in questions" :key="i" >

          <v-card >
            
                <v-card-title
                  class="text-h5"
                 >Pregunta {{i+1}}</v-card-title>
                <v-card-text>{{item[`Question_${$i18n.locale}`]}}</v-card-text>

                <!-- <v-card-subtitle >

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
                </v-card-subtitle>                 -->
            
          </v-card>
         <br/>
        </div>
        </v-col>

        <v-col
          cols="9"
          v-if="selected_network && selected_network.name==='Actor'"
        >
          <v-data-table
                :headers="tableHeader"
                :items="selected_colleagues"
                :items-per-page="5"
                class="elevation-1"
                v-if="selected_colleagues.length>0"
          >
              <template v-slot:item="{ item }">

                <tr>
                      <td class="text-xs-left">{{ item.username }}</td>
                      <td class="text-xs-left">{{ item.organization_area.Organization_area }}</td>
                        <template >
                          <td v-for="(question,index) in mainStore.questions" :key="index">
                            
                          <v-select
                              :id="`sel_${selected_network_mode_theme}_${question.id_question}_${item.id}`"
                              v-model="answers[`${selected_network_mode_theme}_${question.id_question}_${item.id}`]"
                              :items="JSON.parse(question.question_possible_answers.Question_possible_answers)"
                              item-text="texto"
                              item-value="valor"
                              clearable
                              @change="setAnswersArray($event,item.id,question.id_question)"
                              multiple
                              deletable-chips
                              small-chips
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
                                      color="orange"
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


        <v-col
          cols="9"
          v-if="selected_network && selected_network.name!=='Actor'"
        >
          <v-data-table
                :headers="tableHeader"
                :items="nodes"
                :items-per-page="5"
                class="elevation-1"
                v-if="nodes"
          >
              <template v-slot:item="{ item }">

                <tr>
                      <td class="text-xs-left">{{ item.username }}</td>
                      <td class="text-xs-left">{{ item.organization_area.Organization_area }}</td>
                        <template >
                          <td v-for="(question,index) in mainStore.questions" :key="index">
                            
                          <v-select
                              :id="`sel_${selected_network_mode_theme}_${question.id_question}_${item.id}`"
                              v-model="answers[`${selected_network_mode_theme}_${question.id_question}_${item.id}`]"
                              :items="JSON.parse(question.question_possible_answers.Question_possible_answers)"
                              item-text="texto"
                              item-value="valor"
                              clearable
                              @change="setAnswersArray($event,item.id,question.id_question)"
                              multiple
                              deletable-chips
                              small-chips
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
                                      color="orange"
                                  >
                                      mdi-delete
                                  </v-icon>
                              </template>
                              <span>Eliminar</span>
                          </v-tooltip>
                      </td>
                  </tr>
              
              </template>
            
          </v-data-table>

        </v-col>



    </v-row>

    </v-container>
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
        questions:[],
        answers:{},
        nodes:[],
       
        //interactingColleagues:[],

        defaultHeader:[
          {
            text: 'Nombre',
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

          let filteredArr = this.mainStore.network_modes.filter(item =>  item.id_network===this.selected_network.id && item.network_mode_theme);
          
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
            return this.makeTableHeader(this.questions, this.defaultHeader, 'Pregunta');

        },
    
      ...mapStores(useMainStore),

    },


    methods:{

      setAnswersArray(event,employee_id,question_id){

        console.log(event);

        this.$set(this.answers, `${this.selected_network_mode_theme}_${question_id}_${employee_id}`, event);

        console.log(this.answers);
        
        // console.log(event);
        // console.log(employee_id);
        // console.log(question_id);

      },

      makeTableHeader(val, defaultHeader, text) {

            let headers = Object.assign([], defaultHeader);
            //console.log('entro a makeTableheader');

            if (val && val.length > 0) {
           //   console.log(val.length);
                //headers.splice(2, 1);
                val.forEach((question, index) => {
                    headers.splice(2 + index, 0, {
                        text: `${text} ${index + 1}`,
                        align: 'center',
                        sortable: false,
                    });
                });
            }

            return headers.reduce((acc, val) => acc.concat(val), []); //flattens the array
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
          this.questions=[];
          this.nodes=[];

        },


        clearVariables(){

          this.questions=[];
          this.selected_network_mode_theme=null;
          this.nodes=[];

        },

        async getNodes(network_mode_id){

          const nodes = await this.$axios.get(process.env.VUE_APP_BACKEND_URL+'/network_mode/'+network_mode_id +'/nodes');
          this.nodes = nodes.data;

        },

        async getNetworkModeQuestions(selected_network_mode){

          if(selected_network_mode){
            const resp = await this.$axios.get(process.env.VUE_APP_BACKEND_URL+'/network_mode/'+selected_network_mode +'/questions');
            this.questions=resp.data;
          }   

        },


       async getQuestions(){

        let network_mode=null;
        this.questions=[];
        if(this.selected_network && this.selected_network.name==='Actor' && this.filteredNetwokModeThemes) {

          if(this.selected_network_mode_theme){
             network_mode = this.mainStore.network_modes.filter(item =>  item.id_network===this.selected_network.id && item.id_network_mode_theme===this.selected_network_mode_theme)[0];
          }
        }
        else if(this.selected_network && this.selected_network.name!=='Actor'){
          
          network_mode = this.mainStore.network_modes.filter(item =>  item.id_network===this.selected_network.id)[0];
          await this.getNodes(network_mode.id_network_mode);
         
        }

        if(network_mode){
          this.getNetworkModeQuestions(network_mode.id_network_mode)
        }
        
       } 
    }
  }
</script>

