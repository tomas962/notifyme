import Vue from 'vue'
import Vuex from 'vuex'
import {CarList} from '@/store/modules/cars'
import {User} from '@/store/modules/user'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    CarList,
    User
  }
})
