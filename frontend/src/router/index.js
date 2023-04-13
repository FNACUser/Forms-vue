import Vue from 'vue'
import Router from 'vue-router'

import RequestPasswordReset from '@/views/Auth/RequestPasswordReset.vue'
import ResetPasswordForm from '@/views/Auth/ResetPasswordForm.vue'
import { useMainStore } from '@/store/main'
import pinia from "@/store/createPinia";

import ActiveSource from '@/views/ActiveSource.vue'
import DataWise from '@/views/DataWise.vue'
import Culture from '@/views/Culture.vue'
import Login from '@/views/Auth/Login'


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
      path: '/active_source',
      name: 'ActiveSource',
      component: ActiveSource,
      beforeEnter: ifAuthenticated
    },
    {
      path: '/culture',
      name: 'Culture',
      component: Culture,
      beforeEnter: ifAuthenticated
    },
    {
      path: '/datawise',
      name: 'Datawise',
      component: DataWise,
      beforeEnter: ifAuthenticated
    }
    // {
    //   path: '/about',
    //   name: 'About',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue')
    // }
  ]
});


router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
      // this route requires auth, check if logged in
      // if not, redirect to login page.
      // if (!Vue.prototype.$auth.isLoggedIn()) {

      if ((typeof (localStorage.getItem('access_token')) == 'undefined') || (localStorage.getItem('access_token') == null)) {
          next({
              path: '/login',
              query: {redirect: to.fullPath}
          })
      } else {
          next()
      }
  } else {
      next() // make sure to always call next()!
  }
});

export default router;