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
        <v-card-title class="headline">
          <div class="headerClass">
              {{ $t('globals.add') }} {{ label }}
          </div>
            
        </v-card-title>

        <v-card-text>
            <v-form
                    ref="form"
                    v-model="valid"
                    lazy-validation
                >
                    <v-text-field
                        v-model="name"
                        
                        :rules="nameRules"
                        :label="$t('active_source.item_name',{item:`${this.label}`})"
                        required
                    ></v-text-field>
        
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
            @click="saveNode"
          >
          {{ $t('globals.add') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>

</template>


<script>

import { useMainStore } from '@/store/main';
import { mapState} from 'pinia';

export default {

    props:[
        'label',
        'network_mode'    
    ],  
    data () {
      return {
        maxChars:100,
        dialog: false,
        valid:false,
        name:'',
        items:[],
        selected_item:null,
        nameRules: [
            v => !!v || this.$t('rules.field_required'),
            v => (v && v.length <= this.maxChars) || this.$t('rules.length_max_chars', {max_chars:`${this.maxChars}`}),
        ]
      }
    },

    computed:{

    ...mapState(useMainStore,[ "logged_user"])

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

      saveNode(){

       
        if (this.validate()){

         
          const data={
                  "name_es":this.name,
                  "name_en":this.name,
                  "user_email":this.logged_user.email,
                  "network_mode_id":this.network_mode.id_network_mode,
                  "node_segment_id":this.network_mode.id_node_segment
                                 
              };

               this.$axios.post(process.env.VUE_APP_BACKEND_URL+'/node/add', data)
                .then(async response => {
                    //console.log(response.data.response);

                    const nodes= response.data.response;                 
                    this.$alertify.success(this.$t(response.data.message));
                    this.reset();
                    this.resetValidation();
                    this.$emit('newnode',nodes);
                  
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

<style>

.headerClass{
    white-space: nowrap ;
    word-break: normal;
    overflow: hidden ;
    text-overflow: ellipsis;
}
</style>
