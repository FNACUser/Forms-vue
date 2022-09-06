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
        v-if="mainStore.isLoggedIn"
        app
      >

        <v-app-bar-nav-icon @click.stop="drawer = !drawer" v-if="mainStore.isLoggedIn"/>
        <v-spacer></v-spacer>
        <v-toolbar-items v-if="mainStore.isLoggedIn">

                <v-btn text v-if="mainStore.isLoggedIn">{{ mainStore.user.name }}</v-btn>
                <LocaleSwitcher/>
                <v-btn icon @click="mainStore.logout" v-if="mainStore.isLoggedIn">
                    <v-icon>mdi-logout</v-icon>
                </v-btn>

            </v-toolbar-items>

      </v-app-bar>

        <header>
          <link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900" rel="stylesheet">
          <link href="https://cdn.jsdelivr.net/npm/@mdi/font@6.x/css/materialdesignicons.min.css" rel="stylesheet">
          
        </header>
        <v-main>
         
              <router-view ></router-view>
         
        </v-main>

        <v-footer app>
          
        </v-footer>

         </v-app>
</template>

<script>
 
 
 import { useMainStore } from '@/store/main'
 import { mapStores} from 'pinia'
 import LocaleSwitcher from './components/LocaleSwitcher.vue';

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
                
                {
                    icon: "mdi-account_balance",
                    text: this.$t('menus.culture'), 
                    route: "About",
                    roles: ["Admin"]
                }
            ]
        };
    },
    
    created() {
        if (this.mainStore.isLoggedIn) {
            this.mainStore.initialize();
            this.mainStore.setLoggedUser();
        }
    },

    computed: {
        ...mapStores(useMainStore),
    },

    watch:{

      '$i18n.locale'(){

       this.translateMenus();


      },

    },
    methods: {

      translateMenus(){

        this.menus[0].text=this.$t('menus.active_source');
        this.menus[1].text=this.$t('menus.culture');

      }
        
    },
    components: { LocaleSwitcher }
}

</script>

<style>

</style>

