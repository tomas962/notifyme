<template>
  <div>
      <b-row>
          <b-col>
            <b-form @submit="onSubmit">
                <b-form-group
                    id="input-group-1"
                    label="Email address:"
                    label-for="input-1"
                >
                    <b-form-input
                    id="input-1"
                    v-model="email"
                    type="email"
                    required
                    placeholder="Email address"
                    ></b-form-input>
                </b-form-group>
                    <b-form-input v-model="password" type="password" id="text-password" aria-describedby="password-help-block"></b-form-input>
            </b-form>
          </b-col>
      </b-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class Login extends Vue {
    email = ""
    password = ""

    onSubmit(evt: Event) {
        evt.preventDefault()
        console.log(this.email);
        console.log(this.password);
    }
    
}   
</script>

<style scoped lang="scss">

</style>
