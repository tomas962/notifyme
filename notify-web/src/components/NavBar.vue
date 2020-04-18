<template>
<div>
  <b-navbar type="dark" variant="dark">
    <b-container>
        <b-navbar-nav>
          <b-nav-item><router-link to="/">Home</router-link></b-nav-item>
          <b-nav-item><router-link to="/cars">Cars</router-link></b-nav-item>
          <b-nav-item><router-link to="/logout">Logout</router-link></b-nav-item>
        </b-navbar-nav>
    </b-container>
  </b-navbar>
</div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import  'bootstrap-vue'

@Component
export default class MyNavBar extends Vue {
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
