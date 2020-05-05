import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import CarList from '../views/CarList.vue'
import Login from '../views/Login.vue'
import CarQueries from '../views/CarQueries.vue'
import CarView from '@/views/CarView.vue'
import RegisterView from '@/views/RegisterView.vue'
import SettingsView from '@/views/SettingsView.vue'

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
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
