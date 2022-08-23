import Vue from 'vue'
import Router from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from '../views/Auth/Login'

Vue.use(Router)

const router = new Router({
  
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login,
      //beforeEnter: ifNotAuthenticated
    },
    {
      path: '/',
      name: 'home',
      component: HomeView
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
