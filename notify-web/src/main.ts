import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import ElementUI from "element-ui"
import 'element-ui/lib/theme-chalk/index.css';
import Lingallery from 'lingallery';
import '@/assets/main.css'
Vue.component('lingallery', Lingallery);
declare global {
  interface Window { SERVER_URL: string; eventBus: Vue; SCRAPE_INTERVAL: number }
}

window.SERVER_URL = "http://192.168.100.7:5000"
window.eventBus = new Vue();
window.SCRAPE_INTERVAL = 600;

Vue.use(ElementUI)
// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

