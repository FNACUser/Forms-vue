<template>
  <div class="text-xs-center">
    
    <v-dialog
      v-model="loader"
      hide-overlay
      persistent
      width="300"
    >
      <v-card
        color="primary"
        dark
      >
        <v-card-text>
          {{$t('menus.loading')}}
          <v-progress-linear
            indeterminate
            color="white"
            class="mb-0"
          ></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { useMainStore } from '@/store/main'
import { mapState } from 'pinia'

export default{

computed:{
  ...mapState(useMainStore,[ 'loader']),

}


}




</script>


