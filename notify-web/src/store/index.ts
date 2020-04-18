import Vue from 'vue'
import Vuex from 'vuex'
import {CarList} from '@/store/modules/cars'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    SERVER_URL: "http://localhost:5000"
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    CarList
  }
})
