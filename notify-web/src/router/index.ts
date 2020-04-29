import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import Home from '../views/Home.vue'
import CarList from '../views/CarList.vue'
import Login from '../views/Login.vue'
import CarQueries from '../views/CarQueries.vue'

Vue.use(VueRouter)

  const routes: Array<RouteConfig> = [
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
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
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
