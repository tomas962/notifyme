<template>
  <div id="app">
    <MyNavBar />
    <b-container>
      <router-view/>
    </b-container>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import MyNavBar from '@/components/NavBar.vue'
import JWT from 'jwt-decode';
import {namespace} from 'vuex-class'
import {Identity, UserState} from '@/store/modules/user'
const userns = namespace('User')

@Component({
  components: {
    MyNavBar
  }
})
export default class App extends Vue {
  @userns.Action
  setUser!: (state: UserState) => void;


  created(){ //if token exists in localStorage set user info in Vuex
    console.log("APP CREATED");
    const access_token = localStorage.getItem("access_token")
    const refresh_token = localStorage.getItem("refresh_token")
    if (access_token) {
      const decoded_token: any = JWT(access_token);
      const timestamp = Date.now() / 1000 | 0;
      if (timestamp > decoded_token.exp){
        console.log("EXPIRED");
        return
      }
      
      const user_identity: Identity = decoded_token.identity
      const user_state: UserState = {
        identity: user_identity,
        access_token: access_token,
        refresh_token: refresh_token || ""
      }
      
      this.setUser(user_state);
    }
  }
}
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  background-color: #212935;
  color: aliceblue;
  min-height: 100vh;
}

html { 
  background-color: #212935;
}

body {
  min-height: 100vh;
  padding: 0;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
