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

        <b-row class="mt-2">
            <b-col sm="3"></b-col>
            <b-col  cols="6" sm="3" class="text-center mt-1">
                Tiesioginiai pranešimai į įrenginį (ang. "Push Notifications")
            </b-col>
            <b-col cols="6" sm="3" class="text-center">
                <b-form-checkbox @input="pushNotifInput" v-model="notificationsEnabled" v-b-tooltip.hover title="Jei neleidžia įjungti, patikrinkite savo naršyklės pranešimų nustatymus." switch size="lg">
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
    notificationsSupported = false
    email_notifications = 0
    notificationsEnabled = false

    called = false
    async created() {
        if ('Notification' in window && 'serviceWorker' in navigator) {
            this.notificationsSupported = true
            this.notificationsEnabled = Notification.permission === "granted"
        }
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

    async pushNotifInput() {
        if (this.called)
            return
        this.called = true
        setTimeout(() => {this.called = false}, 70)
        if (this.notificationsSupported) {
            const result = await Notification.requestPermission();
            console.log("result:");
            console.log(result);
            if (result === 'granted') {
                this.notificationsEnabled = true
                console.log("before SUBSCRIBED");
                await this.subscribeUser();
                console.log("SUBSCRIBED");
                
            }
            else 
                this.notificationsEnabled = false
        }
    }

    async changePw() {
        console.log("changing passowrd");
        console.log(this.password);

        if (this.password.new_password !== this.password.confirm_password) {
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
        if (this.called)
            return
        this.called = true
        setTimeout(() => {this.called = false}, 70)
        fetch(window.SERVER_URL + "/users/" + this.$store.state.User.identity.user_id + '/settings', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + this.$store.state.User.access_token,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({email_notifications: this.email_notifications})
        })
    }

    async subscribeUser() {
        if ('serviceWorker' in navigator) {
            const reg = await navigator.serviceWorker.ready;
            const publicKeyBytes = [0x04,0x3d,0xdd,0x3d,0x83,0x7c,0x54,0x03,0xde,0x5c,0x27,0x4a,0xe8,0x71,0x75,
            0xf1,0xff,0x25,0x65,0x49,0x8d,0x6a,0x8a,0x06,0x14,0x27,0x85,0x9c,0x71,0xde,
            0x0d,0xa1,0x92,0x7d,0x48,0x63,0xe5,0x10,0x83,0x42,0x36,0xe7,0x9f,0x33,0xe7,
            0xb6,0x2e,0x29,0x57,0x40,0x84,0x48,0x62,0x16,0x1c,0xa0,0x4d,0x15,0x5a,0x6d,
            0x7c,0xa1,0x22,0x4c,0xf4]
            const key = new Uint8Array(65)
            for (let i = 0; i < key.length; i++) {
                key[i] = publicKeyBytes[i]
            }
            const sub =  await reg.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: key
            })
            console.log('Endpoint URL: ', sub.endpoint);
            console.log(JSON.stringify(sub));
            console.log("fetch push_auth");
                
            const response = await fetch(window.SERVER_URL + `/users/${this.$store.state.User.identity.user_id}/push_auth`, {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer ' + this.$store.state.User.access_token,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({auth_json: JSON.stringify(sub)})
            })
        }
    }
}
</script>
<style lang="scss" scoped>

</style>