<template>
  <div>
      <b-alert variant="danger" :show="showErr"  v-on:dismissed="showErr=false" dismissible>{{errMsg}}</b-alert>
      <b-alert variant="success" :show="showSucc" v-on:dismissed="showSucc=false" dismissible>{{succMsg}}</b-alert>
      <b-row class="mt-5">
          <b-col class="border rounded" offset="1" cols="10" sm="8" offset-sm="2" md="6" offset-md="3" lg="4" offset-lg="4">
            <b-form @submit="onSubmit">
                    <h1 class="mb-3 mt-3">Prisijungimas</h1>
                    <b-form-input
                    id="input-1"
                    v-model="email"
                    type="email"
                    required
                    placeholder="El. paštas"
                    ></b-form-input>

                    <b-form-input 
                    v-model="password" 
                    type="password"
                    id="text-password"
                    aria-describedby="password-help-block"
                    class="mt-3"
                    placeholder="Slaptažodis"
                    required
                    ></b-form-input>

                    <b-row>
                        <b-col cols="7" lg="7" xl="8"></b-col>
                        <b-col
                        cols="1" class="mt-3 mr-5 mb-3" 
                        >
                            <b-button
                            class=" btn btn-info"
                            type="submit"
                            >Patvirtinti</b-button>
                        </b-col>
                    </b-row>
                    <b-row>
                        <b-col class="mb-2">
                            <router-link to="/register">Registracija</router-link>
                        </b-col>
                    </b-row>
            </b-form>
          </b-col>
      </b-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import JWT from 'jwt-decode';
import {namespace} from 'vuex-class'
import {UserState} from '../store/modules/user'
const userns = namespace('User')

@Component
export default class Login extends Vue {
    email = ""
    password = ""
    errMsg: string|null = null
    succMsg: string|null = null
    showErr = false
    showSucc = false
    @userns.Action
    setUser!: (state: UserState) => void;

    created() {
        if ((this.$root as any).reg_success) {
            this.succMsg = (this.$root as any).reg_success;
            (this.$root as any).reg_success = undefined;
            this.showSucc = true;
        }
        if ((this.$root as any).login_err) {
            this.errMsg = (this.$root as any).login_err;
            (this.$root as any).login_err = undefined;
            this.showErr = true;
        }
    }

    async onSubmit(evt: Event) {
        evt.preventDefault()
        this.showErr = false

        const response = await fetch(window.SERVER_URL+"/auth", { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({email: this.email, password: this.password})
        })
        
        if (!response.ok) {
            this.errMsg = "Neteisingas el. paštas arba slaptažodis!"
            this.showErr = true
            return
        }
        
        const result = await response.json()

        localStorage.setItem("access_token", result.access_token);
        const decoded_token = (JWT(result.access_token) as any)
        const timestamp = (Date.now() / 1000) | 0;
        setTimeout(() => {
            if (localStorage.getItem("access_token")){
                console.log('jwt expired, deleting');
                
                localStorage.removeItem("access_token");
                this.$router.push('/login');
                (this.$root as any).login_err = "Baigėsi sesija, prisijunkite iš naujo."
            }
        }, ((decoded_token.exp - timestamp) * 1000))

        window.socket.emit("join", {"access_token":result.access_token}, (connected: boolean) => {
            if (connected)
                console.log("socketio connected succesfully");
            else 
                console.log("failed socketio connection");
                
        })
        localStorage.setItem("refresh_token", result.refresh_token);
        const state: UserState = {
            // eslint-disable-next-line
            identity: decoded_token.identity, 
            access_token: result.access_token,
            refresh_token: result.refresh_token
        } 
        this.setUser(state)
        this.$router.push('/queries')
        
    }
    
}   
</script>

<style scoped lang="scss">

</style>
