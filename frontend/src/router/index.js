import Vue from 'vue'
import Router from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from '../views/Auth/Login'
import { useMainStore } from '../store/main'
import { createPinia } from 'pinia'


const pinia = createPinia();

const ifNotAuthenticated = (to, from, next) => {

  const mainStore = useMainStore(pinia);

  
  
  if (!mainStore.isLoggedIn) {
      //console.log('ifnotauth : no está logueado!!')
      next()
      return
  }
  next('/login')
}

const ifAuthenticated = (to, from, next) => {

  const mainStore = useMainStore(pinia);

  console.log(mainStore);

  if (mainStore.isLoggedIn) {
      next()
      return
  }
  if (router.path !== '/login') {
    next('/login')
  }

}

Vue.use(Router)

const router = new Router({


  mode: "history",
  
  routes: [

    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
      beforeEnter: ifNotAuthenticated
    },
    {
      path: '/home',
      name: 'home',
      component: HomeView,
      beforeEnter: ifAuthenticated
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
  ]
})

export default router;
