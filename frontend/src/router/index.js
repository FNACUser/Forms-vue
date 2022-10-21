import Vue from 'vue'
import Router from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import Login from '@/views/Auth/Login'
import RequestPasswordReset from '@/views/Auth/RequestPasswordReset.vue'
import ResetPasswordForm from '@/views/Auth/ResetPasswordForm.vue'
import { useMainStore } from '@/store/main'
import pinia from "@/store/createPinia";


const ifNotAuthenticated = (to, from, next) => {

  const mainStore = useMainStore(pinia);

  if (!mainStore.isLoggedIn) {
      
      next()
      return
  }
  next('/login')
}

const ifAuthenticated = (to, from, next) => {

  const mainStore = useMainStore(pinia);

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
      path: '/forgot-password',
      name: 'forgot-password',
      component: RequestPasswordReset,
      meta: {
        auth:false
      }
    },
    {
      path: '/reset-password/:email/:token',
      name: 'reset-password-form',
      component: ResetPasswordForm,
      meta: {
        auth:false
      }
    },
    {
      path: '/home',
      name: 'Home',
      component: HomeView,
      beforeEnter: ifAuthenticated
    },
    {
      path: '/about',
      name: 'About',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
  ]
})

export default router;