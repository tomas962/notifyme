<template>
    <div>
        <b-alert :show="showErr"  dismissible @dismissed="showErr=false" variant="danger">{{errMsg}}</b-alert>
        <b-alert :show="showSucc"  dismissible @dismissed="showSucc=false" variant="success">{{succMsg}}</b-alert>
        <b-row class="mt-5">
            <b-col offset-sm="3"><h3>Pranešimų nustatymai</h3></b-col>
        </b-row>
        <b-row class="mt-2">
            <b-col sm="3"></b-col>
            <b-col  cols="6" sm="3" class="text-center mt-1">
                Pranešimai į el. paštą. 
            </b-col>
            <b-col cols="6" sm="3" class="text-center">
                <b-form-checkbox @input="updateSettings" value="1" unchecked-value="0" v-model.number="email_notifications" v-b-tooltip.hover title="Jei įjungta, pranešimai apie naujus skelbimus siunčiami į el. paštą." switch size="lg">
                </b-form-checkbox>
            </b-col>
            <b-col sm="3"></b-col>
        </b-row>

        <b-row class="mt-5">
        </b-row>
        <b-row class="mt-5">
            <b-col offset-sm="3"><h3>Keisti slaptažodį</h3></b-col>
        </b-row>
        
        <b-form @submit.prevent="changePw">
        <b-row class="mt-2">
            <b-col offset-sm="3" sm="6" md="4" offset-md="4" offset="2" cols="8">
                <b-input required v-model="password.old_password" type="password" placeholder="Senas slaptažodis"></b-input>
                <b-input required v-model="password.new_password" class="mt-2" type="password" placeholder="Naujas slaptažodis"></b-input>
                <b-input required v-model="password.confirm_password" class="mt-2" type="password" placeholder="Patvirtinti naują slaptažodį"></b-input>
            </b-col>
        </b-row>
        <b-row>
            <b-col cols="6"></b-col>
            <b-col class="mt-2 ml-5">
                <b-button type="submit" variant="success">Patvirtinti</b-button>
            </b-col>
        </b-row>
        </b-form>
    </div>
</template>
<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

interface Passwords {
    old_password: string;
    new_password: string;
    confirm_password: string;
}

@Component
export default class SettingsView extends Vue {
    password: Passwords = {
        old_password: "",
        new_password: "",
        confirm_password: ""
    }
    errMsg = ""
    succMsg = ""
    showErr = false
    showSucc = false

    email_notifications = 0

    async created() {
        const response = await fetch(window.SERVER_URL + "/users/" + this.$store.state.User.identity.user_id + '/settings', {
            headers: {
                'Authorization': 'Bearer ' + this.$store.state.User.access_token,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const data = await response.json();
            this.email_notifications = data.email_notifications
        }
    }



    async changePw() {
        console.log("changing passowrd");
        console.log(this.password);

        if (this.password.old_password !== this.password.confirm_password) {
            this.showErr = true
            this.errMsg = "Slaptažodžiai nesutampa!"
        }

        const response = await fetch(window.SERVER_URL + '/changepw', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + this.$store.state.User.access_token,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.password)
        })

        if (response.ok) {
            this.password = {
                old_password: "",
                new_password: "",
                confirm_password: ""
            }
            this.showSucc = true
            this.succMsg = "Slaptažodis sėkmingai pakeistas"
        } 
        else if (response.status === 403) {
            this.showErr = true
            this.errMsg = "Neteisingas slaptažodis"
        }        
        else {
            this.showErr = true
            this.errMsg = "Slaptažodis nepakeistas: Įvyko klaida keičiant slaptažodį"
        }
    }

    updateSettings() {
        fetch(window.SERVER_URL + "/users/" + this.$store.state.User.identity.user_id + '/settings', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + this.$store.state.User.access_token,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({email_notifications: this.email_notifications})
        })
    }
}
</script>
<style lang="scss" scoped>

</style>