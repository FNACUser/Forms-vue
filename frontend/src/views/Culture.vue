<template>

    <v-container  fluid>
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
                  @change="initialize"
                  @click:clear="resetSelectedVariables"
                  dense
                ></v-select>
            </v-col>
            
            <v-col
              cols="3"
              class="d-flex justify-space-around mb-6 align-end"
              v-if="mainStore.selected_cycle"
            >

              <v-select
                  v-model="selected_theme"
                  :items="themes"
                  :label="$t('culture.themes')"
                  :item-text="`Culture_mode_theme_${$i18n.locale}`"
                  item-value="id"
                  return-object
                  clearable
                  @change="getThemeQuestions"
                  @click:clear="resetSelectedVariables"
                  dense
                ></v-select>
              
            </v-col>
             
        </v-row>

        <v-row v-if="themes.length && Object.keys(totals).length">
          <v-col
              cols="2"
              
              v-for="(theme, index) in themes" :key="index"
              >
                <progress-bars 
                :name="theme[`Culture_mode_theme_${$i18n.locale}`]" 
                :now="totals[`${mainStore.selected_cycle}_${theme.id}`]['now']"
                :preferred="totals[`${mainStore.selected_cycle}_${theme.id}`]['preferred']"
                
                />
                
          </v-col> 
        </v-row> 

        <v-row>

          <v-col>
              <v-card 
                  v-if="selected_theme"
                  
                >
                  <v-toolbar
                    color="primary"
                    dark
                  >
                  

                    <v-toolbar-title><h3>{{ selected_theme[`Questions_prefix_${$i18n.locale}`]}}</h3></v-toolbar-title>

                    <v-spacer></v-spacer>

      
                  
                  </v-toolbar>

      
                  <v-data-table
                    :headers="headers"
                    :items="questions"
                    hide-default-header
                    hide-default-footer
                    dense
                    
                  >

                  <template v-slot:body.prepend>
                    <tr>
                        <td ></td>
                        <td width="150px">
                          <div class="d-flex align-center justify-center ">
                            <h3>{{$t('culture.now')}}</h3>
                          </div>
                          
                        </td>
                      
                        <td width="150px"> 
                          <div class="d-flex align-center justify-center ">
                            <h3>{{$t('culture.preferred')}}</h3>
                          </div>  
                        </td>

                    </tr>
                  </template>

                  <template v-slot:item="{ item }" >

                              <tr>
                                  <td><h3>{{ item[`Culture_mode_theme_question_${$i18n.locale}`] }}</h3></td>
                                  
                                  <td width="150px">
                                    <div class="d-flex align-center ">

                    
                                      <vuetify-money
                                        v-model="answers[`${mainStore.selected_cycle}_${selected_theme.id}_${item.id}`]['now']"
                                        :options="percentOptions"
                                        solo
                                        class="centered-input text--darken-3 mt-8"
                                        
                                        
                                        v-if="answers[`${mainStore.selected_cycle}_${selected_theme.id}_${item.id}`]"
                                      />


                                    </div>
                                   
                                  </td>
                                
                                  <td width="150px"> 
                                    <div class="d-flex align-center ">

                                      <vuetify-money
                                        v-model="answers[`${mainStore.selected_cycle}_${selected_theme.id}_${item.id}`]['preferred']"
                                        :options="percentOptions"
                                        solo
                                        class="centered-input text--darken-3 mt-8"
                                       
                                        v-if="answers[`${mainStore.selected_cycle}_${selected_theme.id}_${item.id}`]"
                                      />
                                </div>
                                    
                                  </td>
                                 
                              
                              </tr>
                  </template>
                  <template v-slot:body.append>
                    <tr>
                        <td ><div class="d-flex justify-end align-center"><h2>TOTAL</h2></div></td>
                        <td width="150px">
                         
                          <div class="d-flex justify-center align-center ">
                            <h2>{{ total_sums['now']/100 | percent }}</h2> 
                          </div>
                          <span  v-if="total_sums['now']>100" style="color:red;">La suma debe ser igual a 100%</span>
                        </td>
                      
                        <td width="150px"> 
                          <div class="d-flex justify-center align-center ">
                            <h2>{{ total_sums['preferred']/100 | percent }}</h2>
                          </div>  
                          <span  v-if="total_sums['preferred']>100" style="color:red;">La suma debe ser igual a 100%</span>
                        </td>

                    </tr>
                  </template>

                  </v-data-table>

                </v-card>
                
          </v-col>

        </v-row>
       
            
    </v-container>
  
</template>
<script>

import { useMainStore } from '@/store/main'
import { mapStores} from 'pinia'
import {numbersFormatMixin} from '../mixins/numbersFormatMixin'
import ProgressBars from '@/components/ProgressBars.vue';

  export default {

    components: { 
      ProgressBars
    },
    mixins: [numbersFormatMixin],

    data() {
      return {

        selected_mode:1,
        selected_theme:null,
        selected_question:null,
        
        questions:[],
        themes:[],
        answers:{},
        totals:{},
        
        editedItem:{
          preferred:null,
          iva:null
        },

        headers: [
          {
            text: '',
            align: 'start',
            value: 'Pregunta',
          },
          { text: 'Ahora', value: '', align: 'center',width: '50px'},
          { text: 'Preferido', value: '',align: 'center' ,width: '50px'},
          
        ],
         

      }
    },

    mounted(){





    },

    watch: {

      total_sums: {
            handler(new_val) {

              // console.log('OLD_VALUE='+JSON.stringify(old_val));
              // console.log('NEW_VALUE='+JSON.stringify(new_val));
                if (new_val && (new_val['now'] || new_val['preferred'])) {

                  if ((new_val['now']==100 && new_val['preferred']==100) && 
                  (new_val['now']!=this.totals[`${this.mainStore.selected_cycle}_${this.selected_theme.id}`]['now'] ||
                   new_val['preferred']!=this.totals[`${this.mainStore.selected_cycle}_${this.selected_theme.id}`]['preferred'])){

                      this.saveCultureAnswers();

                  }

            
                  if(!this.totals[`${this.mainStore.selected_cycle}_${this.selected_theme.id}`]){

                      this.$set(this.totals, `${this.mainStore.selected_cycle}_${this.selected_theme.id}`, new_val);
                  }
                  else{
                    this.totals[`${this.mainStore.selected_cycle}_${this.selected_theme.id}`]=Object.assign({},new_val);

                  }             
                  //console.log(val);
                }
            },
           // deep: true
        }

},

   

    computed:{

      ...mapStores(useMainStore),

      total_sums(){

        let sums = {
          'now':0, 
          'preferred':0
        };

       if(this.questions && this.answers){


        this.questions.forEach(question => {

         
          if(this.mainStore.selected_cycle && this.selected_theme && this.answers[`${this.mainStore.selected_cycle}_${this.selected_theme.id}_${question.id}`]){
            sums['now'] += Number.parseInt(this.answers[`${this.mainStore.selected_cycle}_${this.selected_theme.id}_${question.id}`]['now']);
            sums['preferred'] += Number.parseInt(this.answers[`${this.mainStore.selected_cycle}_${this.selected_theme.id}_${question.id}`]['preferred']);

          }

        })

    
       }

       return  sums;
      },    
     
    },


    methods:{


      initTotals(){

       // console.log('entra a initTotals');
       // console.log(this.themes);
        this.themes.forEach(theme=>{

         // console.log(theme.id)

          if(!this.totals[`${this.mainStore.selected_cycle}_${theme.id}`]){

            //console.log('entra a IF de initTotals');
              this.$set(this.totals, `${this.mainStore.selected_cycle}_${theme.id}`, {'now':0,'preferred':0});
            }

        })
        
       // console.log(this.totals);
      },


      saveCultureAnswers(){

        let final_answers=[];

        this.questions.forEach(question=>{

            const anws_obj={
              'question_id':question.id,
              'now':this.answers[`${this.mainStore.selected_cycle}_${this.selected_theme.id}_${question.id}`]['now'],
              'preferred':this.answers[`${this.mainStore.selected_cycle}_${this.selected_theme.id}_${question.id}`]['preferred']

            }

            final_answers.push(anws_obj);

        });


        const data={
                  "cycle_id":this.mainStore.selected_cycle,
                  "mode_id" : this.selected_mode,
                  "theme_id" : this.selected_theme.id,
                  "answers" : final_answers,
                  "user_email":this.mainStore.logged_user.email
                  
              };

              console.log(data);

               this.$axios.post(process.env.VUE_APP_BACKEND_URL+'/culture/save_answers', data)
                .then(async response => {
                    console.log(response.data);
                    
                    this.$alertify.success(this.$t(response.data.message));
                  
          
                  })
                .catch(error => {
                    this.$alertify.error(this.$t(error.message));
                    console.error('There was an error!', error.message);
                    console.error( error);
              });





      },


      resetSelectedVariables(){



      },

      async initialize(){

        await this.getModeThemes();

        this.initTotals();
        
      },


      async getModeThemes(){

        const response = await this.$axios.get(process.env.VUE_APP_BACKEND_URL+'/culture/mode/'+this.selected_mode +'/themes');
      
        this.themes=response.data;

      },


     async getThemeQuestions(){

      if(this.selected_theme){

          const response = await this.$axios.get(process.env.VUE_APP_BACKEND_URL+'/culture/theme/'+this.selected_theme.id +'/questions');

          this.questions=response.data;

          this.setReactivityInAnswersAndTotalsObjects(this.mainStore.selected_cycle,this.selected_theme.id,this.questions);


          }


      },


      setReactivityInAnswersAndTotalsObjects(cycleID, themeID, questions){

        questions.forEach( question => {

          //console.log(this.answers);


          if(!this.answers[`${cycleID}_${themeID}_${question.id}`]){

             this.$set(this.answers, `${cycleID}_${themeID}_${question.id}`, {'now':0,'preferred':0});
            
          }

        });

        if(!this.totals[`${cycleID}_${themeID}`]){

          this.$set(this.totals, `${cycleID}_${themeID}`, {'now':0,'preferred':0});
        }
      
    
      }


      
    

    }


  }
</script>

<style scoped>

.centered-input >>> input {
      text-align: center
    }

</style>



