<template>
    <div>
      
      
    <v-progress-linear
      color="light-blue"
      height="10"
      :value="now"
      striped
    ></v-progress-linear>
    <br>
    <v-progress-linear
      color="light-green darken-4"
      height="10"
      :value="preferred"
      striped
    ></v-progress-linear>
    
    {{ name }}
   
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