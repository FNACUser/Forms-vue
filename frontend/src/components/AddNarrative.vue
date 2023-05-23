<template>
   <div >
    <v-dialog
      v-model="dialog"
      width="500"
      @click:outside="close"
    >
      <template v-slot:activator="{ on, attrs }">

        <v-btn
            color="primary"
            class="mb-2"
            dark
            v-bind="attrs"
            v-on="on"
        >
        {{  dialog_label }}
        </v-btn>
      </template>

      <v-card>
        <v-card-title class="text-h5 grey lighten-2">
            {{  dialog_label }}
        </v-card-title>

        <v-card-text>
            <v-form
                    ref="form"
                    v-model="valid"
                    lazy-validation
            >
              <v-text-field
                  v-model="title"
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
            color="default"
            text
            @click="cancel"
          >
            {{ $t('globals.cancel') }}
          </v-btn>
           <v-btn
              color="primary"
              text
              @click="saveNarrative"
            >
            {{ action_text }}
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

  props: {
    showNarrativeDialog: { default: false },
    mode:String,
    label:String,
    network_mode_id: Number,
    item:Object   
  },  
    data () {
      return {
        maxChars:55,
        valid:false,
        title: '',
        narrative: '',
        dialog:false,
       
        nameRules: [
            v => !!v || this.$t('rules.field_required'),
            // v => (v && v.length <= this.maxChars) || this.$t('rules.length_max_chars', {max_chars:`${this.maxChars}`}),
          ],
        
      }
  },

  watch: {
    showNarrativeDialog: {

      handler: function (val) {

        this.dialog = val

      },
      // deep: true,
       immediate:true

    },

    mode: {

      handler: function (val) {

        if (val === 'edit') {
          // console.log(val);
          this.title = this.item.title,
          this.narrative = this.item.narrative
        }

      },
      // deep: true,
      immediate: true

    },
  },
  computed: {
      

    ...mapState(useMainStore, ["logged_user", "selected_cycle"]),
        
    ...mapStores(useMainStore),

    action_text() {

      return this.mode === 'create' ? this.$t('globals.add') : this.$t('globals.update');
      
    },

    dialog_label() {

      return this.action_text + ' ' + this.label;
    }

  
  },

  methods: {
      
    validate() {
        
        return this.$refs.form.validate()
      },
    reset() {
        
        this.$refs.form.reset()
      },
    resetValidation() {
        
        this.$refs.form.resetValidation()
      },


    saveNarrative() {

      if (this.mode === 'create') {
        this.createNarrative();
    
      }
      else {
        this.updateNarrative();
      }
   
    },
    

    createNarrative() {
        
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
            
                  const narrative= response.data.response; 
                  this.$alertify.success(this.$t(response.data.message));
                  this.$emit('new_narrative', narrative);
                  this.close();

            
                  })
                .catch(error => {
                    this.$alertify.error(this.$t(error.message));
                    console.error('There was an error!', error.message);
                    console.error( error);
                    this.close();
              });

              
        }  
    },
      

      updateNarrative() {

        if (this.validate()) {

          const data = {
            "narrative_id":this.item.id,
            "title": this.title,
            "narrative": this.narrative,
            "cycle_id": this.mainStore.selected_cycle,
            "user_email": this.logged_user.email,
            "network_mode_id": this.network_mode_id
          };

          this.$axios.post(process.env.VUE_APP_BACKEND_URL + '/user/narrative/update', data)
            .then(async response => {

              // const narrative = response.data.response;
              
              this.$alertify.success(this.$t(response.data));
              this.$emit('narrative_updated',data);
              this.close();
            })
            .catch(error => {
              this.$alertify.error(this.$t(error.message));
              console.error('There was an error!', error.message);
              console.error(error);
              this.close();
            });
        }
      },


      close() {

        this.reset();
        this.resetValidation();
        this.$emit('close');
        this.dialog = false;
      },

      cancel(){
        this.close();

      }
    },
   
  }

</script>
