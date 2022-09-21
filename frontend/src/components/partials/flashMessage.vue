<template>
    <div >
        <v-row >
            <v-col
                md="6"
                offset-md="3"
            >
                <v-alert
                    :type="flash_message_type"
                   
                    text
                    dismissible
                    v-if="flash_message"
                    @input="onClose"
                >
                    {{flash_message}}
                </v-alert>

            </v-col>
           
        </v-row>

    </div>
</template>

<script>

import { useMainStore } from '@/store/main'
import { mapActions,mapState } from 'pinia'

export default {
    

    computed: {

        ...mapState(useMainStore,[ 'flash_message' , 'flash_message_type']),
        
    },

    watch: {
        flash_message(new_val){
            if(new_val){
                setTimeout(()=>{ this.setFlashMessage({});},5000);
            }
        }
    },

    methods:{

        ...mapActions(useMainStore, ['setFlashMessage']),
       

        onClose() {
            this.setFlashMessage({});
        }
    }

}
</script>
