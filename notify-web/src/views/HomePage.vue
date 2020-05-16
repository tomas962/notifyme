<template>
  <div>
      <b-row class="mt-5">
          <b-col class="text-center">
            <h4>Sveiki atvyke, pasirinkite, kurių skelbimų norite ieškoti:</h4>
          </b-col>
      </b-row>
      <b-row class="mt-5">
          <b-col class="text-center">
            <router-link :to="`/users/${$store.state.User.identity.user_id}/queries`"><h3>Automobilių</h3></router-link>
          </b-col>
          <b-col class="text-center">
            <router-link :to="`/users/${$store.state.User.identity.user_id}/re_queries`"><h3>Nekilnojamojo turto</h3></router-link>
          </b-col>
      </b-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class HomePage extends Vue {
    
    
}   
</script>

<style scoped lang="scss">

</style>
