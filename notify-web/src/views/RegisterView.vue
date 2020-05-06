<template>
  <div>
      <b-alert variant="danger" :show="showErr" v-on:dismissed="showErr=false" dismissible>{{errMsg}}</b-alert>
      <b-row class="mt-5">
          <b-col class="border rounded" offset="1" cols="10" sm="8" offset-sm="2" md="6" offset-md="3" lg="4" offset-lg="4">
            <b-form @submit="onSubmit">
                    <h1 class="mb-3 mt-3">Registracija</h1>
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
                    class="mt-3"
                    placeholder="Slaptažodis"
                    required
                    ></b-form-input>

                    <b-form-input 
                    v-model="passwordConfirm" 
                    type="password"
                    class="mt-3"
                    placeholder="Pakartoti slaptažodį"
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
            </b-form>
          </b-col>
      </b-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class RegisterView extends Vue {
    email = ""
    password = ""
    passwordConfirm = ""
    errMsg: string|null = null
    showErr = false

    async onSubmit(evt: Event) {
        evt.preventDefault()
        this.showErr = false;
        if (this.password !== this.passwordConfirm) {
            this.errMsg = "Slaptažodžiai nesutampa!";
            this.showErr = true;
            return;
        }
        const response = await fetch(window.SERVER_URL+"/register", { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({email: this.email, password: this.password, confirm_password: this.passwordConfirm})
        })

        if (response.status === 409) {
            this.errMsg = "Paskyra su šiuo el. pašto adresu jau užregistruota!";
            this.showErr = true;
            return;
        }
        if (!response.ok) {
            this.errMsg = "Registracija nesėkminga!";
            this.showErr = true;
            return;
        } else {
            (this.$root as any).reg_success = "Registracija sėkminga. Prisijunkite."
            this.$router.push('/login')
        }

        

    }
    
}   
</script>

<style scoped lang="scss">

</style>
