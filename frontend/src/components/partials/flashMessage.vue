<template>

        <v-row >
            <v-col
                md="6"
                offset-md="3"
            >
                <v-alert
                    :type="flash_message_type"
                    outlined
                    text
                    dismissible
                    v-if="flash_message"
                    @input="onClose"
                >
                    {{flash_message}}
                </v-alert>

            </v-col>

        </v-row>


</template>

<script>

import {mapMutations, mapState} from 'vuex'

export default {
    data: () => ({

    }),

    computed: {
        ...mapState([
            'flash_message' , 'flash_message_type'
        ]),
    },

    watch: {
        flash_message(new_val){
            if(new_val){
                setTimeout(()=>{ this.setFlashMessage({});},5000);
            }
        }
    },

    methods:{
        ...mapMutations([
            'setFlashMessage'
        ]),

        onClose() {
            this.setFlashMessage({});
        }
    }

}
</script>

<style scoped>

</style>
