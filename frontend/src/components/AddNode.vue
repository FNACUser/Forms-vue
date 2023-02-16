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
                        v-model="name_es"
                        :counter="10"
                        :rules="nameRules"
                        label="Texto en español"
                        required
                    ></v-text-field>

                    <v-text-field
                        v-model="name_en"
                        :counter="10"
                        :rules="nameRules"
                        label="Texto en inglés"
                        required
                    ></v-text-field>

                    <v-select
                        v-model="selected_item"
                        :items="items"
                        :rules="[v => !!v || 'Item is required']"
                        label="Item"
                        required
                    ></v-select>

                
                    
                </v-form>

        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
            @click="dialog = false"
          >
          {{ $t('globals.add') }}
          </v-btn>

          <v-btn
            color="default"
            text
            @click="dialog = false"
          >
          {{ $t('globals.cancel') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>

</template>


<script>


export default {

    props:[
        'label'     
    ],  
    data () {
      return {
        dialog: false,
        valid:false,
        name_es:'',
        name_en:'',
        items:[],
        selected_item:null,
        nameRules: [
            v => !!v || 'Name is required',
            v => (v && v.length <= 10) || 'Name must be less than 10 characters',
        ],
      }
    },

    methods: {
      validate () {
        this.$refs.form.validate()
      },
      reset () {
        this.$refs.form.reset()
      },
      resetValidation () {
        this.$refs.form.resetValidation()
      },
    },
   
  }

</script>
