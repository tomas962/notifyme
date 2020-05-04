<template>
    <div>
        <div id="app">
            <MyNavBar />
            <b-container>
                <router-view />
            </b-container>
            <div
                id="to-top-btn"
                class="border rounded"
                v-if="showScrollButton"
                v-on:click="scrollUp"
            >
                <b-icon-chevron-double-up class="mt-3 ml-3" scale="3"></b-icon-chevron-double-up>
            </div>
            <footer
                id="footer"
                class="text-center font-italic font-weight-bold mt-2"
            >Tomas Čižauskas @ 2020</footer>
        </div>
    </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import MyNavBar from "@/components/NavBar.vue";
import JWT from "jwt-decode";
import { namespace } from "vuex-class";
import { Identity, UserState } from "@/store/modules/user";
const userns = namespace("User");

@Component({
    components: {
        MyNavBar
    }
})
export default class App extends Vue {
    @userns.Action
    setUser!: (state: UserState) => void;

    @userns.Action
	watchToken!: () => void;

    showScrollButton = false;
    created() {
        //if token exists in localStorage set user info in Vuex
        console.log("APP CREATED");
        const access_token = localStorage.getItem("access_token");
        const refresh_token = localStorage.getItem("refresh_token");
        if (access_token) {
            const decoded_token: any = JWT(access_token);
            const timestamp = (Date.now() / 1000) | 0;
            if (timestamp > decoded_token.exp) {
                console.log("EXPIRED");
                localStorage.removeItem("access_token");
                return;
            }

            const user_identity: Identity = decoded_token.identity;
            const user_state: UserState = {
                identity: user_identity,
                access_token: access_token,
                refresh_token: refresh_token || ""
            };

            this.setUser(user_state);
        } else if (refresh_token) {
			const decoded_token: any = JWT(refresh_token);
			console.log("ACCESS_TOKEN EXPIRED, REFRESH_TOKEN:");
			console.log(decoded_token);
			
        }

        setInterval(() => {
            this.showScrollButton =
                (window.pageYOffset || document.documentElement.scrollTop) >
                800;
        }, 500);
    }

    scrollUp() {
        window.scrollTo({
            top: 0,
            left: 0,
            behavior: "smooth"
        });
    }
}
</script>

<style lang="scss">
$background-color: #1c2023;
$font-color: aliceblue;

#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    // background-color: #212935;
    background-color: $background-color;
    color: $font-color;
    min-height: 100vh;
}

html {
    // background-color: #212935;
    background-color: $background-color;
}

body {
    min-height: 100vh;
    padding: 0;
    margin-bottom: 20px;
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

#to-top-btn {
    position: fixed;
    bottom: 10%;
    right: 10%;
    width: 50px;
    height: 50px;
    cursor: pointer;
}

#to-top-btn:hover {
    color: rgb(89, 89, 233);
}

.pointer {
    cursor: pointer;
}

.hoverable {
    transition: background-color 0.5s;
}

.hoverable:hover {
    background-color: lighten($background-color, 10%);
}

#footer {
    text-align: center;
    background-color: $background-color;
    color: $font-color;
    height: 30px;
    bottom: 0;
    left: 45%;
}
</style>
