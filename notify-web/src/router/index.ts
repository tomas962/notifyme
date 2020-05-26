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
import ReAdList from '@/views/ReAdList.vue'
import ReAdView from '@/views/ReAdView.vue'
import HomePage from '@/views/HomePage.vue'
import UsersView from '@/views/UsersView.vue'

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
    path: '/users/:user_id/queries/:query_id/cars',
    name: 'Cars',
    component: CarList
  },
  {
    path: '/users/:user_id/re_queries/:query_id/re_ads',
    name: 'ReAds',
    component: ReAdList
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/users/:user_id/queries',
    name: 'Queries',
    component: CarQueries
  },
  {
    path: '/users/:user_id/queries/:query_id/cars/:car_id',
    name: 'CarView',
    component: CarView
  },
  {
    path: '/register',
    name: 'RegisterView',
    component: RegisterView
  },
  {
    path: '/users/:user_id/settings',
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
  {
    path: '/users/:user_id/re_queries/:query_id/re_ads/:re_ad_id',
    name: 'ReAdView',
    component: ReAdView
  },
  {
    path: '/',
    name: 'HomePage',
    component: HomePage
  },
  {
    path: '/users',
    name: 'UsersView',
    component: UsersView
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  if (!localStorage.getItem("access_token") && to.path !== '/login' && to.path !== '/register')
    next({ path: '/login' })
  else
    next()
})

export default router
