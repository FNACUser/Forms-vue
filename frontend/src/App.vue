<template>

    <v-app>
      <v-navigation-drawer 
        v-model="drawer"
        :clipped="$vuetify.breakpoint.lgAndUp"
        v-if="mainStore.isLoggedIn"
        app
      >
      <v-list dense>
        <template v-for="item in menus">

              <v-list-group
                  v-if="item.children "
                  :key="item.text"

                  :prepend-icon="item.icon"
                  :append-icon="item['icon-alt']"
              >
                  <template v-slot:activator>
                      <v-list-item-content>
                          <v-list-item-title>
                              {{ item.text }}
                          </v-list-item-title>
                      </v-list-item-content>
                  </template>


                  <v-list-item
                      v-for="(child, i) in item.children"
                      :key="i"
                      :to="{name:child.route}"

                  >
                      <v-list-item-action v-if="child.icon">
                          <v-icon>{{ child.icon }}</v-icon>
                      </v-list-item-action>
                      <v-list-item-content>
                          <v-list-item-title>
                              {{ child.text }}
                          </v-list-item-title>
                      </v-list-item-content>

                  </v-list-item>

              </v-list-group>

              <v-list-item
                  v-else
                  :key="item.text"
                  :to="{name:item.route}"

              >
                  <v-list-item-action>
                      <v-icon>{{ item.icon }}</v-icon>
                  </v-list-item-action>
                  <v-list-item-content>
                      <v-list-item-title>
                          {{ item.text }}
                      </v-list-item-title>
                  </v-list-item-content>
              </v-list-item>
          </template>
        </v-list>
       
      </v-navigation-drawer>
      <v-app-bar 
        :clipped-left="$vuetify.breakpoint.lgAndUp"
        color="primary"
        app
        
      >
    
        <v-app-bar-nav-icon @click.stop="drawer = !drawer" v-if="mainStore.isLoggedIn"  style="color: white;"/>
            
        <v-spacer></v-spacer>
        <v-toolbar-items v-if="mainStore.isLoggedIn">
                <LocaleSwitcher/>
                <v-btn text  class="white--text">{{ mainStore.logged_user.name }}</v-btn>
                <v-btn icon @click="mainStore.logout" style="color: white;">
                    <v-icon>mdi-logout</v-icon>
                </v-btn>

        </v-toolbar-items>
        <v-toolbar-items v-else>

            <LocaleSwitcher/>
            
        </v-toolbar-items>

      </v-app-bar>

        <header>
          <link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900" rel="stylesheet">
          <link href="https://cdn.jsdelivr.net/npm/@mdi/font@6.x/css/materialdesignicons.min.css" rel="stylesheet">
          
        </header>
        <v-main>
            
                <vue-particles color="#7afff6"/>
                <flash-message style="height: 8px;"/>
                <router-view ></router-view>
                <loader></loader>  
                      
        </v-main>

        <v-footer app>

           
        </v-footer>

         </v-app>
</template>

<script >

 import { useMainStore } from '@/store/main'
 import { mapStores} from 'pinia'
 import LocaleSwitcher from './components/LocaleSwitcher.vue';
 import Loader from './components/partials/_loader';
 import flashMessage from './components/partials/flashMessage';


 export default{
    data() {
        return {
            drawer: true,
            menus: [
                { 
                  icon: "mdi-list",
                  text: this.$t('menus.active_source'), 
                  route: "Home", 
                  roles: ["Admin"]
                },
                
                // {
                //     icon: "mdi-account_balance",
                //     text: this.$t('menus.culture'), 
                //     route: "About",
                //     roles: ["Admin"]
                // }
            ]
        };
    },

    
    components: { 
        LocaleSwitcher,
        Loader,
        flashMessage,
       
    },
    
    created() {
        if (this.mainStore.isLoggedIn) {
            this.mainStore.initialize();
            this.mainStore.setLoggedUser();
        }

        this.$axios.interceptors.request.use((config) => {
            // Do something before request is sent
            this.mainStore.loader= true;
            return config;
        }, (error) => {
            // Do something with request error
            this.mainStore.loader = false;
            return Promise.reject(error);
        });

        // Add a response interceptor
        this.$axios.interceptors.response.use((response) => {
            // Do something with response data
            this.mainStore.loader = false;
            return response;
        }, (error) => {
            // Do something with response error
            this.mainStore.loader=false;
            return Promise.reject(error);
        });
    },
    mounted() {
      
    },

    computed: {
        ...mapStores(useMainStore),
    },

    watch:{

    //   '$i18n.locale'(){

    //    this.translateMenus();


    //   },

    },
    methods: {

      translateMenus(){

        this.menus[0].text=this.$t('menus.active_source');
        this.menus[1].text=this.$t('menus.culture');

      }  
    }
}

</script>

<style scoped>

#particles-js { 
  /*position: absolute;
  background-size: cover;
  top: 0; 
  bottom: 0; 
  left: 0;
  right: 0; 
  overflow-y: hidden; 
  z-index: 0;*/
  width: 100%;
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 0; 
}

.v-data-table {
    position: absolute;
}

</style>

