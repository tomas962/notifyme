<template>
<div style="background-color: #343a40;">
<b-container>
    <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand href="#">NotifyMe</b-navbar-brand>
    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
    <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
            <b-nav-item to="/login" v-if="identity.email == ''">Prisijungti</b-nav-item>
            <b-nav-item v-if="identity.email" to="/queries">Automobiliai</b-nav-item>
            <b-nav-item v-if="identity.email" :to="`/users/${identity.user_id}/messages`">Pranešimai</b-nav-item>
        </b-navbar-nav>
        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <b-nav-item>Sveiki, {{identity.email || 'svečias'}}</b-nav-item>
          <b-nav-item v-if="identity.email" to="/settings">Nustatymai</b-nav-item>
          <b-nav-item v-if="identity.email" v-on:click="logout();" >Atsijungti</b-nav-item>
        </b-navbar-nav>
    </b-collapse>
    </b-navbar>
</b-container>
</div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import {namespace} from 'vuex-class'
import {Identity, UserState} from '../store/modules/user'
const userns = namespace('User')

@Component
export default class MyNavBar extends Vue {
  @userns.State
  public identity!: Identity;

  @userns.Action
  public setUser!: (state: UserState) => void;

  logout() {
    console.log("logging out user");
    const state: UserState = {
      identity: new Identity(),
      access_token: "",
      refresh_token: ""
    };
    this.setUser(state)
    localStorage.removeItem("access_token")
    localStorage.removeItem("refresh_token")
    this.$router.push("/login")
  }
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
