<template>

    <v-container  class="px-10" fluid>
      <br/>
        <v-row >
          <v-col
            class="d-flex justify-space-around mb-6 align-end"
            cols="2"
          >
            <v-select
              v-model="mainStore.selected_cycle"
              :items="mainStore.filteredCycles"
              :label="$t('globals.period')"
              :item-text="`Cycle_${$i18n.locale}`"
              item-value="id_cycle"
              clearable
             
              dense
            ></v-select>
          </v-col>
        
          <v-col
              cols="2"
              class="d-flex justify-space-around mb-6 align-end"
              >
                <v-autocomplete
                  v-model="selected_topic"
                  :items="topics"
                  :label="$t('datawise.topics')"
                  :item-text="`name_${$i18n.locale}`"
                  item-value="id"
                  clearable 
                  dense
                  
                ></v-autocomplete>
            </v-col>
        
            <v-col
              class="d-flex justify-space-around mb-6 align-end"
              cols="3"
              v-if="selected_topic"
            >
              <v-autocomplete
                v-model="selected_tools"
                :items="filteredTools"
                item-text="`name_${$i18n.locale}`"
                item-value="id"
                :label="$t('datawise.tools')"
                persistent-hint
                small-chips
                multiple
                return-object
                @change="addToolToList()"
                dense
               
              ></v-autocomplete>
            </v-col>  
                     
        </v-row>
        <!-- <v-row v-if="mainStore.network_modes.length">
          <v-col
              cols="2"
              
              v-for="(form, index) in forms" :key="index"
              >
                <gauge 
                    :label="form[`name_${$i18n.locale}`]" 
                    :in_value="Math.round(form['answers']*100/(form['total_questions']*form['total_items']))"
                    :in_size="((current_network_mode && form.id==current_network_mode.id_network_mode) ? 100:60 )"
                    :in_width="((current_network_mode && form.id==current_network_mode.id_network_mode) ? 15:7 )"
                    @click.native="setSelectedNetworkAndTheme(form)"
                
                />
                
          </v-col>  
        </v-row> -->
        <!-- <v-row  v-if="current_network_mode">
          <v-col 
                cols="3" 
            >   
            
                <v-switch
                    v-model="currentForm.is_concluded"
                    :label="`${$t('active_source.section_closed')}: ${getFormSectionName(this.current_network_mode,this.$i18n.locale)}`"
                    @change="toggleOpenCloseCurrentForm"
                    v-if="currentForm"
                  ></v-switch>
                
          </v-col> -->

          <!-- <v-col
            
            v-if="selected_network && selected_network.code!=='actor'"

            class="d-flex justify-end mr-11"
          >
            <add-node
              :label="selected_network[`name_${$i18n.locale}`]"
              :network_mode_id="current_network_mode.id_network_mode"
              @newnode="refreshNodes"
            >
            </add-node> 
          </v-col>

          
          </v-row> -->

        <v-row dense justify="space-around">
          
            <v-col
              cols="8"
            >

              <v-data-table
                    :headers="tableToolsHeader"
                    :items="selected_tools"
                    :items-per-page="-1"
                    class="elevation-1"
                    v-if="selected_tools.length>0"
                    dense
              >
                  <template v-slot:item="{ item }">

                    <tr>
                          <td class="text-xs-left">{{ item.name }}</td>

                            <template >
                              <td v-for="(question,index) in questions" :key="index" class="">
                                
                              <v-select
                                  id="id"
                                  v-model="answers"
                                  items="options"
                                  item-text="texto"
                                  item-value="valor"
                                  clearable
                                  @change="saveAnswersArray($event,item)"
                                  multiple
                                  deletable-chips
                                  small-chips
                                  outlined
                                  flat
                                  rounded
                                  class="my-5"
                                  dense
                                 
                                
                                >                         
                              </v-select>  
                              
                              </td>                         
                            </template>
                          <td >

                              <v-tooltip bottom >
                                  <template #activator="{ on }">
                                      <v-icon
                                          v-on="on"
                                          small
                                          @click="delRecord(item,'menus.delete_record_title','alerts.delete_interacting_person_text',selected_tool[`name_${$i18n.locale}`],'Actor')"
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
            
        </v-row>
        
        <confirmation-dialog ref="confirmDeleteActor"/>
            
    </v-container>
  
</template>
<script>

import { useMainStore } from '@/store/main';
import { mapStores,mapState} from 'pinia';
import ConfirmationDialog from '@/components/partials/ConfirmationDialog.vue';
// import Gauge from '@/components/Gauge.vue';
//import AddNode from '@/components/AddNode.vue';

export default {

    components: { 
      ConfirmationDialog,
      // Gauge,
     // AddNode
    },

    data() {
      return {

        
        selected_topic:null,
        selected_tools:[],
        

        topics:[
          { 
            "id":1,
            "name_es":"Tema1",
            "name_en":"Topic1",
          },
          { 
            "id":2,
            "name_es":"Tema2",
            "name_en":"Topic2",
          },
          { 
            "id":3,
            "name_es":"Tema3",
            "name_en":"Topic3",
          },
          { 
            "id":4,
            "name_es":"Tema4",
            "name_en":"Topic4",
          },
        ],

        tools:[
          { 
            "id":1,
            "name_es":"Herramienta1",
            "name_en":"Tool1",
            "topic_id":1
          },
          { 
            "id":2,
            "name_es":"Herramienta2",
            "name_en":"Tool2",
            "topic_id":1
          },
          { 
            "id":3,
            "name_es":"Herramienta1",
            "name_en":"Tool1",
            "topic_id":2
          },
          { 
            "id":4,
            "name_es":"Herramienta2",
            "name_en":"Tool2",
            "topic_id":3
          },
          { 
            "id":5,
            "name_es":"Herramienta3",
            "name_en":"Tool3",
            "topic_id":3
          },

        ],







       
        selected_node_segment_category:null,
        selected_network_mode_theme:null,
        questions:[],
        answers:{},
        nodes:[],
       
        formClosed:false,
        adjacency_input_forms:[],
        forms:[],

        selRules: [
          
          v => (v && v.length <= 2) || 'Máximo 2 opciones!! ${v.length}',
        ],

        defaultToolsHeader:[
          {
            text: 'Nombre',
            align: 'start',
            value: 'username',
            class: "white--text"
          },
          { 
            text: 'Area', 
            value: 'id_organization_area',
            class: "white--text" 
          },
          
          { 
            text: 'Acciones',
            class: "white--text",
            sortable: false},
        ]


      }
    },

    mounted(){

    //  console.log('entra amounted de ActiveSource');
     // this.initialize();

    },

    watch:{

      selected_cycle(new_val){
          
          if(new_val==null){

          //  console.log('watch en ActiveSource -> cycle is null');
            this.resetSelectedVariables();
          }
          else{

            this.initialize();

          }
      }


    },
   

    computed:{

      ...mapState(useMainStore,[ "selected_cycle"]),
      ...mapStores(useMainStore),


    

      filteredTools(){


        if(this.selected_topic){

          return this.tools.filter(item=> item.topic_id===this.selected_topic); 

        }
        else return null;
        
      },

      

      tableToolsHeader() {
        
            return this.makeToolsTableHeader(this.questions, this.defaultToolsHeader, this.$t('active_source.question'));

        }
    
      

    },


    methods:{


     

      saveAnswersArray(){

         // console.log('Entra a SaveAnswerArray');



      },


      // updateNetworkModeGauge(network_mode){

      //     const index = this.forms.findIndex(item => item.id== network_mode.id_network_mode);
          
      //     const prefix = network_mode.id_network_mode +'_';
         
      //     const num_answers= Object.keys(this.answers).filter(item => item.startsWith(prefix)).length;
         
      //     this.forms[index]['answers'] = num_answers;

      //     if(network_mode.network.code=='actor'){
      //         this.forms[index]['total_items'] = this.selected_actors.length > 0 ? this.selected_actors.length : 1; 
                
      //     }
      //     else{
            
      //       this.forms[index]['total_items'] = this.filteredNodes.length > 0 ? this.filteredNodes.length :  1;      

      //     }        
      // },


      // updateAllActorNetworkModeGauges(){
        
      //   this.mainStore.network_modes.forEach(network_mode => {

      //     if (network_mode.network.code=='actor'){
      //         this.updateNetworkModeGauge(network_mode);
      //     }

      //   })
      
      // },



      makeToolsTableHeader(val, defaultHeader, text) {

            let headers = Object.assign([], defaultHeader);
          
            if (val && val.length > 0) {
           
                val.forEach((question, index) => {
                    headers.splice(2 + index, 0, {
                        text: `${text} ${index + 1}`,
                        align: 'center',
                        class: 'white--text',
                        sortable: false,
                    });
                });
            }

            headers[0].text = this.$t('active_source.actor_table.name');
            headers[1].text = this.$t('active_source.actor_table.area');
            headers[headers.length-1].text = this.$t('active_source.actor_table.actions');


            return headers;

           
        },



      async addToolToList(){

      
         

      },


      
      async deleteTool(item){

        const item_index = this.selected_actors.findIndex(object => {
                return object.id==item.id
              });
        this.selected_actors.splice(item_index,1);

      },



      resetSelectedVariables(){

          this.selected_area=null;
          this.mainStore.selected_cycle=null;
          this.selected_actors=null;
          this.selected_network=null;
          this.selected_node_segment_category=null;
          this.selected_network_mode_theme=null;
          this.questions=[];
          this.nodes=[];
          this.current_network_mode=null;
          this.answers=[];
          this.mainStore.network_modes=[];
          this.forms=[];

        },


        clearVariables(){

          this.questions=[];
          this.selected_network_mode_theme=null;
          this.current_network_mode=null;
          this.nodes=[];
         
        },

        async getNodes(network_mode_id){

          if(network_mode_id){

            const nodes = await this.$axios.get(process.env.VUE_APP_BACKEND_URL+'/network_mode/'+network_mode_id +'/nodes');
            this.nodes = nodes.data;
          }
          //return  nodes.data;
         // console.log(this.nodes);

        },


       async getActors(){

          await this.$axios.get(process.env.VUE_APP_BACKEND_URL+'/user/'+this.mainStore.logged_user.id+'/cycle/'+this.mainStore.selected_cycle+'/interacting_actors')
              .then(response => {
                const actor_ids = response.data;
                this.selected_actors = this.mainStore.employees.filter(item =>  actor_ids.includes(item.id));
              })
              .catch(error => {
                
                console.error('There was an error!', error.message);
              });

        },


      async initialize(){

        if(this.mainStore.selected_cycle){
       
          // await this.getActors();
          // await this.mainStore.getNetworkModes(this.mainStore.selected_cycle);
          // await this.getUserResponses();
          // await this.createFormsDetails();

        }


      }
    }


  }
</script>

<style>

.v-data-table-header {
  background: #2196f3!important;
}

.v-data-table { 
  overflow-x: auto;
}

</style>

