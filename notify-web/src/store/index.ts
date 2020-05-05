import Vue from 'vue'
import Vuex from 'vuex'
import {CarList} from '@/store/modules/cars'
import {User} from '@/store/modules/user'
import {UIState} from '@/store/modules/ui_state'

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
    User,
    UIState
  }
})
