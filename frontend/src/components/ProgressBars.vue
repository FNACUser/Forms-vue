<template>
    <div>   
      <v-progress-linear
        :color="isSelected ? 'light-blue darken-4':'light-blue'"
        :height="isSelected ? 30:18"
        :value="now"
        striped
        :class="now!=100 ? 'red--text': isSelected ? 'white--text' : 'black--text'"
      >
      <strong>{{ now }}</strong>
      </v-progress-linear>
      <br>
      <v-progress-linear
        :color="isSelected ? 'light-green darken-4':'light-green'"
        :height="isSelected ? 30:18"
        :value="preferred"
        striped
        :class="preferred!=100 ? 'red--text': isSelected ? 'white--text' : 'black--text'"
      >
      <strong>{{ preferred }}</strong>
      </v-progress-linear>
    
      <strong v-if="isSelected">{{ name }}</strong>
      <div v-else>
        {{ name }}
      </div>
   
    </div>

</template>


<script>


export default {

  props:[
          'name', 
          'now', 
          'preferred',
          'isSelected'
    ],  


    data () {
      return {
        
      }
    },
   
    mounted () {
     
    },

    computed:{

      


    },

    watch: {
      
    },
  }




</script>