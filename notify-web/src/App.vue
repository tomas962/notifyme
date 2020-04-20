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
@Component({
  components: {
    MyNavBar
  }
})
export default class App extends Vue {
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
