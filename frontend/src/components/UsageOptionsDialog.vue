<template>
    <div >

        <v-form ref="form" v-model="valid_form" lazy-validation>
            <v-dialog
                v-model="openDialog"
                max-width="800px"
                @click:outside="close"
            >

              
              <v-card class="mx-auto">
                <v-card-title>
                  <span class="headline">{{ $t('active_source.usage_options') }}</span>
                </v-card-title>
                <v-card-text>
                  <v-container grid-list-md>

                 
                    <v-checkbox 
                      v-for="(option, index) in usageOptions" :key="index"
                      :value="option['id']"
                      :label="option[`name_${$i18n.locale}`]" 
                      v-model="selected_options" 
                    >
                    </v-checkbox>
                    

                  </v-container>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                    
                    <v-btn color="blue"   dark  @click="close">{{ $t('globals.cancel') }}</v-btn>
                    <v-btn color="success"   @click.native="saveSelectedOptions" >{{ $t('globals.select') }}</v-btn>
                    
                </v-card-actions>
              </v-card>
            </v-dialog>
        </v-form>

  </div>

</template>

<script>

  
    export default {

      name: "UsageOptionsDialog",

      props:[
           
            'showDialog',
            'usageOptions',
            'toolID',
            'questionID',
            'defaultOptions'
            
        ],

      data: () => ({

            openDialog:false,
            valid_form:false ,
            selected_options:[],

        }),


      mounted(){

        // console.log('entra amounted!')

      },

      watch: {

        showDialog: {

            handler: function (val) {

              // console.log(val);

                this.openDialog=val

            },
            // deep: true,
            // immediate:true

        },


        defaultOptions: {

            handler: function (val) {

              this.selected_options = val;

            },
            //  deep: true,
            //  immediate:true

        },

        },

      computed: {

         

        },


      methods: {


          
          close() {

              this.openDialog = false;
              this.selected_options=[];
              this.$emit('close');

            },

          clear() {
            this.$refs.form.reset();
            this.selected_options=[];
           },

          saveSelectedOptions(){

            const data ={
              'selected_options':this.selected_options,
              'toolID':this.toolID,
              'questionID':this.questionID

            }
            this.$emit('usageOptionsSelected', data);
            this.close();


           }

        }
    }
</script>

