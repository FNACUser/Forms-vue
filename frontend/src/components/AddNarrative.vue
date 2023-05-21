<template>
   <div >
    <v-dialog
      v-model="dialog"
      width="500"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
            color="primary"
            class="mb-2"
            dark
            v-bind="attrs"
            v-on="on"
        >
        {{ $t('globals.add') }} {{ label }}
        </v-btn>
      </template>

      <v-card>
        <v-card-title class="text-h5 grey lighten-2">
            {{ $t('globals.add') }} {{ label }}
        </v-card-title>

        <v-card-text>
            <v-form
                    ref="form"
                    v-model="valid"
                    lazy-validation
                >
                    <v-text-field
                        v-model="title"
                        :counter="maxChars"
                        :label="$t('active_source.narrative_title')"
                       
                        :rules="nameRules"
                    ></v-text-field>

                    <v-textarea
                        v-model="narrative"
                        :label="$t('active_source.narrative_description')"
                        
                        :rules="nameRules"
                       
                    ></v-textarea>

                </v-form>

        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
            @click="saveNarrative"
          >
          {{ $t('globals.add') }}
          </v-btn>

          <v-btn
            color="default"
            text
            @click="cancel"
          >
          {{ $t('globals.cancel') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>

</template>


<script>

import { useMainStore } from '@/store/main';
import { mapStores, mapState} from 'pinia';

export default {

    props:[
        'label',
        'network_mode_id'    
    ],  
    data () {
      return {
        maxChars:55,
        dialog: false,
        valid:false,
        title: '',
        narrative:'',
       
        nameRules: [
            v => !!v || this.$t('rules.field_required'),
            // v => (v && v.length <= this.maxChars) || this.$t('rules.length_max_chars', {max_chars:`${this.maxChars}`}),
          ],
        
      }
    },

   

    computed:{

        ...mapState(useMainStore, ["logged_user", "selected_cycle"]),
        ...mapStores(useMainStore)

    },

    methods: {
      validate () {
        return this.$refs.form.validate()
      },
      reset () {
        this.$refs.form.reset()
      },
      resetValidation () {
        this.$refs.form.resetValidation()
      },

      saveNarrative(){

       
        if (this.validate()){

            const data = {
                "title": this.title,
                "narrative": this.narrative,
                "cycle_id": this.mainStore.selected_cycle,
                "user_email":this.logged_user.email,
                "network_mode_id":this.network_mode_id                                 
              };

               this.$axios.post(process.env.VUE_APP_BACKEND_URL+'/user/narrative/add', data)
                .then(async response => {
                    //console.log(response.data.response);

                    const narrative= response.data.response;
                    
                    this.$alertify.success(this.$t(response.data.message));
                    this.reset();
                    this.resetValidation();

                    this.$emit('new_narrative', narrative);

            
                  })
                .catch(error => {
                    this.$alertify.error(this.$t(error.message));
                    console.error('There was an error!', error.message);
                    console.error( error);
                    this.reset();
                    this.resetValidation();
              });

              this.dialog = false;
        }

        
      },


      cancel(){
        this.reset();
        this.resetValidation();
        this.dialog = false;

      }
    },
   
  }

</script>
