<template>
    <div>   
      <v-progress-linear
        color="light-blue"
        height="25"
        :value="now"
        striped
      >
      <strong>{{ now }}</strong>
      </v-progress-linear>
      <br>
      <v-progress-linear
        color="light-green darken-4"
        height="25"
        :value="preferred"
        striped
      >
      <strong>{{ preferred }}</strong>
      </v-progress-linear>
    
      <strong>{{ name }}</strong>
   
    </div>

</template>


<script>


export default {

  props:[
          'name', 
          'now', 
          'preferred'
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