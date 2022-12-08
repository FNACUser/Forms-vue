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
          :label="$t('main_page.period')"
          :item-text="`Cycle_${$i18n.locale}`"
          item-value="id_cycle"
          clearable
          @change="initialize"
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
            :label="$t('main_page.questionaire_type')"
            :item-text="`name_${$i18n.locale}`"
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
            :label="$t('main_page.question_theme')"
            :item-text="`Network_mode_theme_${$i18n.locale}`"
            item-value="id_network_mode_theme"
            clearable
            @change="getQuestions"
            @click:clear="clearVariables"
            
          ></v-select>
      </v-col>
      </v-row>
      <v-row v-if="selected_network && selected_network.code==='actor'"> 
        <v-col
          cols="3"
          class="d-flex justify-space-around mb-6 align-end"
          >
            <v-autocomplete
              v-model="selected_area"
              :items="mainStore.areas"
              :label="$t('main_page.area')"
              :item-text="`Organization_area_${$i18n.locale}`"
              item-value="id_organization_area"
              clearable 
            ></v-autocomplete>
        </v-col>
    
        <v-col
          class="d-flex justify-space-around mb-6 align-end"
          cols="3"
        >
          <v-autocomplete
            v-model="selected_actors"
            :items="filteredEmployees"
            item-text="username"
            item-value="id"
            
            :label="$t('main_page.user')"
            persistent-hint
            
            
            small-chips
            multiple
            return-object
            @change="addInteractingActor()"
          
          ></v-autocomplete>
        </v-col>     
    </v-row>

    <v-row dense justify="space-around">
      <v-col cols="3">
        <div v-for="(item, i) in questions" :key="i" >
          <v-card > 
            <v-app-bar
            flat
            color="blue"
            >          
                <v-card-title
                  class="white--text" 
                 >
                 {{$t('main_page.question')}} {{i+1}}
                </v-card-title>
            </v-app-bar>    
                <v-card-text>{{item[`Question_${$i18n.locale}`]}}</v-card-text>            
          </v-card>
         <br/>
        </div>
        </v-col>
        <v-col
          cols="9"
          v-if="selected_network && selected_network.code==='actor'"
        >
          <v-data-table
                :headers="tableActorsHeader"
                :items="selected_actors"
                :items-per-page="-1"
                class="elevation-1"
                v-if="selected_actors.length>0"
                dense
          >
              <template v-slot:item="{ item }">

                <tr>
                      <td class="text-xs-left">{{ item.username }}</td>
                      <td class="text-xs-left">{{ item.organization_area[`Organization_area_${$i18n.locale}`] }}</td>
                        <template >
                          <td v-for="(question,index) in questions" :key="index" class="">
                            
                          <v-select
                              :id="`sel_${current_network_mode.id_network_mode}_${question.id_question}_${item.id}`"
                              v-model="answers[`${current_network_mode.id_network_mode}_${question.id_question}_${item.id}`]"
                              :items="JSON.parse(question.question_possible_answers[`Question_possible_answers_${$i18n.locale}`])"
                              item-text="texto"
                              item-value="valor"
                              clearable
                              @change="saveAnswersArray($event,item.id,question.id_question)"
                              :multiple="question.question_possible_answers.multiple"
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
                      <td>
                          <v-tooltip bottom>
                              <template #activator="{ on }">
                                  <v-icon
                                      v-on="on"
                                      small
                                      @click="delRecord(item)"
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
          v-if="selected_network && selected_network.code!=='actor'"
        >
          <v-data-table
                :headers="tableNodesHeader"
                :items="nodes"
                :items-per-page="-1"
                class="elevation-1"
                v-if="nodes"
                dense
          >
              <template v-slot:item="{ item }">
                <tr>
                      <td class="text-xs-left">{{ item[`Node_${$i18n.locale}`] }}</td>
                      
                        <template >
                          <td v-for="(question,index) in questions" :key="index">
                            
                          <v-select
                              :id="`sel_${current_network_mode.id_network_mode}_${question.id_question}_${item.id_node}`"
                              v-model="answers[`${current_network_mode.id_network_mode}_${question.id_question}_${item.id_node}`]"
                              :items="JSON.parse(question.question_possible_answers[`Question_possible_answers_${$i18n.locale}`])"
                              item-text="texto"
                              item-value="valor"
                              clearable
                              @change="saveAnswersArray($event,item.id_node,question.id_question)"
                              :multiple="question.question_possible_answers.multiple"
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
                      
                </tr>
              </template>
          </v-data-table>
        </v-col>
    </v-row>
    

    <confirmation-dialog ref="confirmDeleteActor">
      
    </confirmation-dialog>
   

    </v-container>
</template>
<script>

import { useMainStore } from '@/store/main'
import { mapStores} from 'pinia'
import ConfirmationDialog from '@/components/partials/ConfirmationDialog.vue';


  export default {

    components: { 
      ConfirmationDialog
    },

    data() {
      return {

        selected_actors:[],
        selected_cycle:null,
        selected_network:null,
        selected_area:null,
        selected_node_segment_category:null,
        selected_network_mode_theme:null,
        questions:[],
        answers:{},
        nodes:[],
        current_network_mode:null,
        selRules: [
          
          v => (v && v.length <= 2) || 'Máximo 2 opciones!! ${v.length}',
        ],

        defaultActorsHeader:[
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
        ],


        defaultNodesHeader:[
          {
            text: 'Nombre',
            align: 'start',
            value: 'name',
            class: "white--text"
          }
        ],


      }
    },

    // mounted(){

    // },
   

    computed:{


      interactingPeopleIds(){


        if(this.selected_actors){

          return this.selected_actors.map(a => a.id);

        }  

        return [];
      },


      filteredCycles(){
        return this.mainStore.cycles.filter(item=> item.Is_active); 
      },

      filteredEmployees(){


        if(this.selected_area){

          return this.mainStore.employees.filter(item=> item.id_organization_area===this.selected_area); 

        }
        else return null;
        
      },

      filteredNetwokModeThemes(){

        if(this.selected_network){

          let filteredArr = this.mainStore.network_modes.filter(item =>  item.id_network === this.selected_network.id && item.network_mode_theme);
          
          if (filteredArr && filteredArr.length){
            return filteredArr.map(item => {
              return item.network_mode_theme;
              
              });
          }
          else return null;
        }
        else 
        return null;

      },

      tableActorsHeader() {
        
            return this.makeActorsTableHeader(this.questions, this.defaultActorsHeader, this.$t('main_page.question'));

        },

      tableNodesHeader() {
        
            return this.makeNodesTableHeader(this.questions, this.defaultNodesHeader, this.$t('main_page.question'));

        },
    
      ...mapStores(useMainStore),

    },


    methods:{



      saveAnswersArray(event,item_id,question_id){

        console.log('Entra a SaveAnswerArray');

        console.log(event);

        // if(event.length>=3){

        //   this.answers[`${this.current_network_mode.id_network_mode}_${question_id}_${employee_id}`].pop();
        // }

        

        //else{



              this.$set(this.answers, `${this.current_network_mode.id_network_mode}_${question_id}_${item_id}`, event);

              const data={
                  "cycle_id":this.selected_cycle,
                  "user_email":this.mainStore.logged_user.email,
                  "item_id":item_id,
                  "question_id":question_id,
                  "network_mode_id":this.current_network_mode.id_network_mode,
                 // "network_mode_theme_id":this.selected_network_mode_theme,
                  "selected_option": event
              };

              this.$axios.post(process.env.VUE_APP_BACKEND_URL+'/save_answer', data)
              .then(response => {
                //console.log(response.data);
                this.$alertify.success(this.$t(response.data));

              }

                )
              .catch(error => {
                this.$alertify.error(this.$t(error.message));
                console.error('There was an error!', error.message);
            });


       // }

      },


      makeActorsTableHeader(val, defaultHeader, text) {

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

            headers[0].text = this.$t('main_page.actor_table.name');
            headers[1].text = this.$t('main_page.actor_table.area');
            headers[headers.length-1].text = this.$t('main_page.actor_table.actions');


            return headers;

           
        },


        makeNodesTableHeader(val, defaultHeader, text) {

          let headers = Object.assign([], defaultHeader);
          
          if (val && val.length > 0) {

              val.forEach((question, index) => {
                  headers.splice(1 + index, 0, {
                      text: `${text} ${index + 1}`,
                      align: 'center',
                      class: 'white--text',
                      sortable: false,
                  });
              });
          }

          headers[0].text = this.selected_network[`name_${this.$i18n.locale}`];
         
          return headers;

          
          },

      sortSelectedColleagues(){
        this.selected_actors.sort((a,b) => 
          (a.username.toLowerCase() < b.username.toLowerCase()) ? -1 : ((b.username.toLowerCase() > a.username.toLowerCase()) ? 1 : 0));

      },



      async addInteractingActor(){

      
          // gets last selected person pushed into the list 
          const data={
              "user_email":this.mainStore.logged_user.email,
              "employee_ids":this.interactingPeopleIds,
              "cycle_id":this.selected_cycle           
          };

    
          await this.$axios.post(process.env.VUE_APP_BACKEND_URL+'/add_interacting_actor', data)
          .then(response => console.log(response.data))
          .catch(error => {
            
            console.error('There was an error!', error.message);
          });

          this.sortSelectedColleagues();

          },


      async delRecord(item) {
        if (
          await this.$refs.confirmDeleteActor.open(
            this.$t('menus.delete_record_title'),
            this.$t('menus.delete_record_text'),
            {color:"red lighten-3"}
          )
        ) {
          await this.deleteActor(item);
        }
      },



      async deleteActor(item) {
           
            let item_index = this.selected_actors.findIndex(object => {
                return object.id==item.id});

            const data={
                  "user_email":this.mainStore.logged_user.email,
                  "item_id":item.id,
                  "cycle_id":this.selected_cycle           
              };
          
            await this.$axios.delete(process.env.VUE_APP_BACKEND_URL+'/delete_interacting_actor', {data:data})
              .then(response => {
                console.log(response.data);
                this.selected_actors.splice(item_index,1);
              })
              .catch(error => {
                
                console.error('There was an error!', error.message);
              });
     
      },


      resetSelectedVariables(){

          this.selected_area=null;
          this.selected_cycle=null;
          this.selected_actors=null;
          this.selected_network=null;
          this.selected_node_segment_category=null;
          this.selected_network_mode_theme=null;
          this.questions=[];
          this.nodes=[];
          this.current_network_mode=null;
          this.answers=[];

        },


        clearVariables(){

          this.questions=[];
          this.selected_network_mode_theme=null;
          this.current_network_mode=null;
          this.nodes=[];
          //this.answers=[]

        },

        async getNodes(network_mode_id){

          const nodes = await this.$axios.get(process.env.VUE_APP_BACKEND_URL+'/network_mode/'+network_mode_id +'/nodes');
          this.nodes = nodes.data;

         // console.log(this.nodes);

        },


       async getActors(){

          await this.$axios.get(process.env.VUE_APP_BACKEND_URL+'/user/'+this.mainStore.logged_user.id+'/cycle/'+this.selected_cycle+'/interacting_actors')
              .then(response => {
                const actor_ids = response.data;
                this.selected_actors = this.mainStore.employees.filter(item =>  actor_ids.includes(item.id));
              })
              .catch(error => {
                
                console.error('There was an error!', error.message);
              });

        },


        async getUserResponses(){

          await this.$axios.get(process.env.VUE_APP_BACKEND_URL+'/user/'+this.mainStore.logged_user.id+'/cycle/'+this.selected_cycle+'/responses')
              .then(response => {
               
                const responses = response.data;

               // console.log(responses);

                if(responses){

                 responses.forEach(response => {

                  const resp_content=JSON.parse(response.Response);

                  //console.log(resp_content);

                  resp_content.forEach(content =>{

                      this.answers[`${response.adjacency_input_form['id_network_mode']}_${response.id_question}_${content.item_id}`]= content.valor
                  })

                 });

                }
                
              })
              .catch(error => {
                
                console.error('There was an error!', error.message);
              });

        },


        async getNetworkModeQuestions(selected_network_mode){

          if(selected_network_mode){
            const resp = await this.$axios.get(process.env.VUE_APP_BACKEND_URL+'/network_mode/'+selected_network_mode +'/questions');
            this.questions=resp.data;
          }   

        },


      async getQuestions(){

            this.questions=[];
            if(this.selected_network && this.selected_network.code==='actor' && this.filteredNetwokModeThemes) {

              if(this.selected_network_mode_theme){
                this.current_network_mode = this.mainStore.network_modes.filter(item =>  item.id_network===this.selected_network.id && item.id_network_mode_theme===this.selected_network_mode_theme)[0];
              }
            }
            else if(this.selected_network && this.selected_network.code!=='actor'){
              
              this.current_network_mode = this.mainStore.network_modes.filter(item =>  item.id_network===this.selected_network.id)[0];
              await this.getNodes(this.current_network_mode.id_network_mode);
            
            }

            if(this.current_network_mode){
              this.getNetworkModeQuestions(this.current_network_mode.id_network_mode)
            }
            
      },

      async initialize(){

        if(this.selected_cycle){

          await this.getActors();
          await this.mainStore.getNetworkModes(this.selected_cycle);
          await this.getUserResponses();
        }


      }
    }


  }
</script>

<style>

.v-data-table-header {
  background: #2196f3!important;
}

</style>

