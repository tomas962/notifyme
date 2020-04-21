<template>
  <div>
      <b-row class="mt-5">
          <b-col class="border rounded" offset="1" cols="10" sm="8" offset-sm="2" md="6" offset-md="3" lg="4" offset-lg="4">
            <b-form @submit="onSubmit">
                    <h1 class="mb-3">Login</h1>
                    <b-form-input
                    id="input-1"
                    v-model="email"
                    type="email"
                    required
                    placeholder="Email address"
                    ></b-form-input>

                    <b-form-input 
                    v-model="password" 
                    type="password"
                    id="text-password"
                    aria-describedby="password-help-block"
                    class="mt-3"
                    placeholder="Password"
                    required
                    ></b-form-input>

                    <b-row>
                        <b-col
                        cols="1" offset="8"
                        >
                            <b-button
                            class="m-3 btn btn-info"
                            type="submit"
                            >Login</b-button>
                        </b-col>
                    </b-row>
            </b-form>
          </b-col>
      </b-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import * as JWT from 'jwt-decode';
import {namespace} from 'vuex-class'
import {Identity} from '../store/modules/user'
const userns = namespace('User')

@Component
export default class Login extends Vue {
    email = ""
    password = ""

    @userns.Action
    setUser!: (state: {identity: Identity; access_token: string; refresh_token: string}) => void;

    onSubmit(evt: Event) {
        evt.preventDefault()
        fetch(window.SERVER_URL+"/auth", { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({email: this.email, password: this.password})
        })
        .then((response) => response.json())
        .then((result: { access_token: string; refresh_token: string }) => {
            this.setUser({
                identity: JWT(result.access_token).identity,
                access_token: result.access_token,
                refresh_token: result.refresh_token
                })
        }).catch((error) => {
            console.log(error);
        });
    }
    
}   
</script>

<style scoped lang="scss">

</style>
