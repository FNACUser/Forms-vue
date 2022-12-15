<template>
    <div>
      
        <v-progress-circular
            :rotate="rotate"
            :size="size"
            :width="width"
            :color="color"
            :value="value"
        >
        {{ value }} %
        
        </v-progress-circular>
        <div>
          <v-chip
            x-small
          >
            {{label}}
          </v-chip>
        
        </div>
        
        
       
    </div>

</template>


<script>

import colors from 'vuetify/lib/util/colors'

export default {

  props:[
          'in_rotate', 
          'in_size', 
          'in_width',
          'in_color',
          'in_value',
          'label',
          'actionItem'
    ],  


    data () {
      return {
        interval: {},
        value: this.in_value??0,
        rotate:this.in_rotate??-90,
        size:this.in_size??70,
        //color:this.in_color??'green',
        width:this.in_width??'7'
      }
    },
    // beforeDestroy () {
    //   clearInterval(this.interval)
    // },
    mounted () {
      // this.interval = setInterval(() => {
      //   if (this.value === 100) {
      //     return (this.value = 0)
      //   }
      //   this.value += 10
      // }, 1000)
    },

    computed:{

      color(){

        let final_color=colors.red.base;
        switch (true) {
              case this.value <= 10:
                final_color=colors.red.base;
                break;
              case this.value <= 20:
                final_color=colors.deepOrange.darken1;
                break;
              case this.value <= 30:
                final_color=colors.orange.accent4;
                break;
              case this.value <= 40:
                final_color=colors.amber.base;
                break;
              case this.value <= 50:
                final_color=colors.yellow.darken1;
                break;
              case this.value <= 60:
                final_color=colors.lime.accent2;
                break;
              case this.value <= 70:
                final_color=colors.lime.lighten1;
                break;
              case this.value <= 80:
                final_color=colors.lime.base;
                break;
              case this.value <= 90:
                final_color=colors.lightGreen.darken1;
                break;
              case this.value < 100:
                final_color=colors.green.darken2;
                break;
              case this.value == 100:
                final_color=colors.indigo.darken4;
                break;
              default:
                final_color=colors.red.base;
            }

            console.log(final_color);

            return  final_color;
      }


    },

    watch: {
      in_value(new_val){
            if(new_val>=0){
                this.value=new_val;
            }
        },

      in_size(new_val){
          if(new_val>=0){
              this.size=new_val;
          }
      },

      in_width(new_val){
          if(new_val>=0){
              this.width=new_val;
          }
      }
    },
  }




</script>