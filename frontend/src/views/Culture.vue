<template>

    <v-container  fluid>
      <br/>
        <v-row >
            <v-col
              class="d-flex justify-space-around mb-6 align-end"
              cols="2"
            >
                <v-select
                  v-model="selected_cycle"
                  :items="filteredCycles"
                  :label="$t('globals.period')"
                  :item-text="`Cycle_${$i18n.locale}`"
                  item-value="id_cycle"
                  clearable
                 
                 
                  dense
                ></v-select>
            </v-col>
            
            <v-col
              cols="3"
              class="d-flex justify-space-around mb-6 align-end"
              v-if="selected_cycle"
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
                 
                  dense
                ></v-select>
              
            </v-col>
             
        </v-row>

        <v-row v-if="selected_cycle && themes.length && Object.keys(totals).length">
          <v-col
              cols="2"
              
              v-for="(theme, index) in themes" :key="index"
              >
                <progress-bars 
                :name="theme ? theme[`Culture_mode_theme_${$i18n.locale}`] : ''" 
                :now="theme ? totals[`${selected_cycle}_${theme.id}`]['now'] : 0"
                :preferred="theme ? totals[`${selected_cycle}_${theme.id}`]['preferred'] : 0"
                :is-selected="selected_theme && theme.id==selected_theme.id"
                @click.native="setSelectedTheme(theme)"
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
                                        v-model="answers[`${selected_cycle}_${selected_theme.id}_${item.id}`]['now']"
                                        :options="integerOptions"
                                        solo
                                        class="centered-input text--darken-3 mt-8"
                                        v-if="answers[`${selected_cycle}_${selected_theme.id}_${item.id}`]"
                                        
                                      />


                                    </div>
                                   
                                  </td>
                                
                                  <td width="150px"> 
                                    <div class="d-flex align-center ">

                                      <vuetify-money
                                        v-model="answers[`${selected_cycle}_${selected_theme.id}_${item.id}`]['preferred']"
                                        :options="integerOptions"
                                        solo
                                        class="centered-input text--darken-3 mt-8"
                                       
                                        v-if="answers[`${selected_cycle}_${selected_theme.id}_${item.id}`]"
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
                            <h2>{{ total_sums['now'] }}</h2> 
                          </div>
                          <span  v-if="total_sums['now']>100" style="color:red;">La suma debe ser igual a 100%</span>
                        </td>
                      
                        <td width="150px"> 
                          <div class="d-flex justify-center align-center ">
                            <h2>{{ total_sums['preferred'] }}</h2>
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
import { mapState, mapWritableState} from 'pinia'
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
        questions:[],
        themes:[],
        answers:{},
        totals:{},
      
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

     // console.log('entro a mounted de Culture');

      this.initialize();
    },

    // created(){
    //   console.log('entro a created');

    // },

    watch: {

      total_sums: {
            handler(new_val) {

              // console.log('OLD_VALUE='+JSON.stringify(old_val));
              // console.log('NEW_VALUE='+JSON.stringify(new_val));
                if (new_val && (new_val['now'] || new_val['preferred'])) {

                  if ((new_val['now']==100 && new_val['preferred']==100) && 
                  (new_val['now']!=this.totals[`${this.selected_cycle}_${this.selected_theme.id}`]['now'] ||
                   new_val['preferred']!=this.totals[`${this.selected_cycle}_${this.selected_theme.id}`]['preferred'])){

                      this.saveCultureAnswers();

                  }

            
                  if(!this.totals[`${this.selected_cycle}_${this.selected_theme.id}`]){

                      this.$set(this.totals, `${this.selected_cycle}_${this.selected_theme.id}`, new_val);
                  }
                  else{
                    this.totals[`${this.selected_cycle}_${this.selected_theme.id}`]=Object.assign({},new_val);

                  }             
                  //console.log(val);
                }
            },
           // deep: true
        },


        selected_cycle(new_val){
          
          if(new_val==null){

         //   console.log('watch en Culture -> cycle is null');
            this.resetSelectedVariables();
          }
          else {

            this.initialize();

          }
        }


},

   

    computed:{

     // ...mapStores(useMainStore),
      ...mapWritableState(useMainStore,[ "selected_cycle"]),

      ...mapState(useMainStore,[ "logged_user","filteredCycles" ]),

      total_sums(){

        let sums = {
          'now':0, 
          'preferred':0
        };

       if(this.questions && this.answers){


        this.questions.forEach(question => {

         
          if(this.selected_cycle && this.selected_theme && this.answers[`${this.selected_cycle}_${this.selected_theme.id}_${question.id}`]){
            sums['now'] += Number.parseInt(this.answers[`${this.selected_cycle}_${this.selected_theme.id}_${question.id}`]['now']);
            sums['preferred'] += Number.parseInt(this.answers[`${this.selected_cycle}_${this.selected_theme.id}_${question.id}`]['preferred']);

          }

        })

    
       }

       return  sums;
      },    
     
    },


    methods:{


      initTotals(){

      
        this.themes.forEach(theme=>{

          if(!this.totals[`${this.selected_cycle}_${theme.id}`]){      
              this.$set(this.totals, `${this.selected_cycle}_${theme.id}`, {'now':0,'preferred':0});
            }

        });

        this.getUserModeThemesTotals(this.logged_user.id, this.selected_cycle,this.selected_mode);


        
       // console.log(this.totals);
      },


      saveCultureAnswers(){

        let final_answers=[];

        this.questions.forEach(question=>{

            const anws_obj={
              'question_id':question.id,
              'now':this.answers[`${this.selected_cycle}_${this.selected_theme.id}_${question.id}`]['now'],
              'preferred':this.answers[`${this.selected_cycle}_${this.selected_theme.id}_${question.id}`]['preferred']

            }

            final_answers.push(anws_obj);

        });


        const data={
                  "cycle_id":this.selected_cycle,
                  "mode_id" : this.selected_mode,
                  "theme_id" : this.selected_theme.id,
                  "answers" : final_answers,
                  "user_email":this.logged_user.email
                  
              };

             // console.log(data);

               this.$axios.post(process.env.VUE_APP_BACKEND_URL+'/culture/save_answers', data)
                .then(async response => {
                  //  console.log(response.data);
                    
                    this.$alertify.success(this.$t(response.data.message));
                  
          
                  })
                .catch(error => {
                    this.$alertify.error(this.$t(error.message));
                    console.error('There was an error!', error.message);
                    console.error( error);
              });

      },

      setSelectedTheme(theme){

       this.selected_theme=theme;
       this.getThemeQuestions();

      },


      resetSelectedVariables(){

        this.questions=[];
        this.themes=[];
        this.selected_theme=null;
      
      },

      async initialize(){

       // console.log('Entra a Initialize de Culture');

        if(this.selected_cycle){

         // console.log('Entra al IF de  Initialize de Culture');

          await this.getModeThemes();
          this.initTotals();

        }

      },


      async getModeThemes(){

        const response = await this.$axios.get(process.env.VUE_APP_BACKEND_URL+'/culture/mode/'+this.selected_mode +'/themes');
      
        this.themes=response.data;

      },


     async getThemeQuestions(){

      if(this.selected_theme){

          const response = await this.$axios.get(process.env.VUE_APP_BACKEND_URL+'/culture/theme/'+this.selected_theme.id +'/questions');

          this.questions=response.data;

          this.setReactivityInAnswersAndTotalsObjects(this.selected_cycle,this.selected_theme.id,this.questions);
          //console.log('antes de llamar a getUserModeThemeAnswers')

          this.getUserModeThemeAnswers(this.logged_user.id, this.selected_cycle,this.selected_mode, this.selected_theme.id)

          
          }


      },

      


      async getUserModeThemeAnswers(user_id, cycle_id, mode_id, theme_id){

    
          if(user_id && cycle_id && mode_id && theme_id){

      

              this.$axios.get(process.env.VUE_APP_BACKEND_URL+'/culture/user/'+user_id+'/cycle/'+cycle_id+'/mode/'+mode_id+'/theme/'+theme_id +'/answers')
                .then(async response => {
                    
                    
                    if(response.data.length){
                      this.initAnswersArrayWithExistingValues(cycle_id, theme_id, response.data)
                    }
                    else{
                      this.$alertify.warning(this.$t(response.data.message));

                    }
       
                  })
                .catch(error => {
                    this.$alertify.error(this.$t(error.message));
                   
              });
              
          }

      },


      initAnswersArrayWithExistingValues(cycle_id, theme_id, ini_values){

        ini_values.forEach(answer =>{

          this.answers[`${cycle_id}_${theme_id}_${answer['id_culture_mode_theme_question']}`]['now']=answer['Actual'];
          this.answers[`${cycle_id}_${theme_id}_${answer['id_culture_mode_theme_question']}`]['preferred']=answer['Preferred'];

        })


      },


      setReactivityInAnswersAndTotalsObjects(cycleID, themeID, questions){

        questions.forEach( question => {

          if(!this.answers[`${cycleID}_${themeID}_${question.id}`]){

             this.$set(this.answers, `${cycleID}_${themeID}_${question.id}`, {'now':0,'preferred':0});
            
          }

        });

        if(!this.totals[`${cycleID}_${themeID}`]){

          this.$set(this.totals, `${cycleID}_${themeID}`, {'now':0,'preferred':0});
        }
    
      },


      async getUserModeThemesTotals(user_id, cycle_id, mode_id){

          if(user_id && cycle_id && mode_id){
              const existing_themes_totals = await this.$axios.get(process.env.VUE_APP_BACKEND_URL+'/culture/user/'+user_id+'/cycle/'+cycle_id+'/mode/'+mode_id+'/themes_totals');

              if(existing_themes_totals.data.length){
                this.initTotalsArrayWithExistingValues(cycle_id, existing_themes_totals.data);
              }
              

          }
      },

      initTotalsArrayWithExistingValues(cycle_id, ini_values){

        ini_values.forEach(value =>{

          this.totals[`${cycle_id}_${value['id_culture_mode_theme']}`]['now']=value['Total_actual'];
          this.totals[`${cycle_id}_${value['id_culture_mode_theme']}`]['preferred']=value['Total_preferred'];

        })


      },
      
    

    }


  }
</script>

<style scoped>

.centered-input >>> input {
      text-align: center
    }

</style>



