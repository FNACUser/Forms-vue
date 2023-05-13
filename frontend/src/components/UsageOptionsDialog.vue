<template>
    <div >

        <v-form ref="form" v-model="valid_form" lazy-validation>
            <v-dialog
                v-model="openDialog"
                max-width="500px"
                @click:outside="close"
            >

              
              <v-card>
                <v-card-title>
                  <span class="headline">Opciones de Uso</span>
                </v-card-title>
                <v-card-text>
                  <v-container grid-list-md>

                    

                  </v-container>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                    <v-btn color="pink"   @click.native="clear" class="ma-2 black--text">Limpiar</v-btn>
                    <v-btn color="blue"   dark  @click="close">Cancelar</v-btn>
                    
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
           
            'showDialog'
        ],

        data: () => ({

            openDialog:false,
            valid_form:false ,
            selected_options:{},

        }),

    watch: {

        showDialog: {

            handler: function (val) {

              // console.log(val);

                this.openDialog=val

            },
            // deep: true,
            // immediate:true


        },

        

        },

        computed: {

         

        },


        methods: {


          
          close() {

              this.openDialog = false;
              this.$emit('close');

            },

          clear() {
            this.$refs.form.reset();
           },

        }
    }
</script>

