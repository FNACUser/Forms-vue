<template>
    <div>


        <v-btn
            :color="color"
            dark
            :size="size"
            >
             
        </v-btn>
    
        
        <div>
          <v-chip
            x-small
          >
            <strong>{{label}}</strong>
          </v-chip>
        
        </div>
        
        
       
    </div>

</template>


<script>


export default {

  props:[
          'in_size', 
          'in_color',
          'label'
    ],  


    data () {
      return {
        interval: {},
        value: this.in_value??0,
        
        size:this.in_size??'large',
        color:this.in_color??'green',
       
      }
    },
   
    mounted () {
      
    },

    computed:{

      suffix_symbol(){
 
        return (this.mode==='percent' ? '%' : '');

      },

      
    },

    watch: {
      in_color(new_val){
            console.log(new_val);
            this.color=new_val;
          
        },

      in_size(new_val){
          if(new_val){
              this.size=new_val;
          }
      }
    },
  }

</script>
<style>
     
     .pointer {
        cursor: pointer;
      }
      
</style>