import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import store from '@/store/index'
import {User} from '@/store/modules/user'
import CarList from '../views/CarList.vue'
import Login from '../views/Login.vue'
import CarQueries from '../views/CarQueries.vue'
import CarView from '@/views/CarView.vue'
import RegisterView from '@/views/RegisterView.vue'
import SettingsView from '@/views/SettingsView.vue'
import MessagesView from '@/views/MessagesView.vue'
import REQueries from '@/views/REQueries.vue'

Vue.use(VueRouter)

  const routes: Array<RouteConfig> = [
  // {
  //   path: '/about',
  //   name: 'About',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  // },
  {
    path: '/queries/:query_id/cars',
    name: 'Cars',
    component: CarList
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/queries',
    name: 'Queries',
    component: CarQueries
  },
  {
    path: '/queries/:query_id/cars/:car_id',
    name: 'CarView',
    component: CarView
  },
  {
    path: '/register',
    name: 'RegisterView',
    component: RegisterView
  },
  {
    path: '/settings',
    name: 'SettingsView',
    component: SettingsView
  },
  {
    path: '/users/:user_id/messages',
    name: 'MessagesView',
    component: MessagesView
  },
  {
    path: '/users/:user_id/re_queries',
    name: 'REQueries',
    component: REQueries
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  //if (!((store.state as any).User as User).identity.email && to.path !== '/login' && to.path !== '/register')
  if (!localStorage.getItem("access_token") && to.path !== '/login' && to.path !== '/register')
    next({ path: '/login' })
  else 
    next()
})

export default router
