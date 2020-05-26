<template>
  <div>
      <h2 class="mt-3">Vartotojai</h2>
    <div class="overflow-auto">
        <b-pagination
        v-model="tableUsers"
        :total-rows="users.length"
        :per-page="perPage"
        aria-controls="msg-table"
        ></b-pagination>
        <b-table id="msg-table" bordered  hover :fields="[
            {key: 'El._paštas', thStyle:''},
            {key: 'Grupė', thStyle:''},
            {key: 'Id', thStyle:'width: 10%'},
            {key: 'Blokuoti', thStyle:'width: 10%'},
        ]" 
        :per-page="perPage"
        :current-page="currentPage"
        responsive class="mt-3" dark :items="tableUsers" >

            <template v-slot:cell(El._paštas)="data">
                {{data.value}}
            </template>

            <template v-slot:cell(Blokuoti)="data">
                <b-btn @click="banUser(data.item.Id, 1)" variant="danger" v-if="data.value === 0 && data.item['Grupė'] !== 'admin'">Blokuoti</b-btn>
                <b-btn @click="banUser(data.item.Id, 0)" variant="success" v-if="data.value === 1 && data.item['Grupė'] !== 'admin'">Atblokuoti</b-btn>
            </template>
        </b-table>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import {User} from '@/models/interfaces'

@Component
export default class UsersView extends Vue {
    users: User[] = []
    currentPage = 1
    perPage = 20
    created () {
        this.getUsers()    
    }

    async getUsers() {
        const response = await fetch(window.SERVER_URL + "/users", {
            headers: {
                'Authorization': 'Bearer ' + this.$store.state.User.access_token
            },
            method: 'GET'
        })

        if (!response.ok) {
            return
        }

        const data = await response.json()
        console.log(data);
        
        this.users = data.reverse()
    }

    get tableUsers(){
        const usrs = this.users.map((user) => {
            
            return {
                "El._paštas": user.email,
                "Grupė": user.user_group,
                "Id": user.id,
                "Blokuoti": user.banned
            }
        })
        return usrs
    }

    async banUser(id: number, banned: number) {
        console.log(id);
        const response = await fetch(window.SERVER_URL + "/users/" + id, {
            headers: {
                'Authorization': 'Bearer ' + this.$store.state.User.access_token,
                'Content-Type': 'application/json'
            },
            method: 'PUT',
            body: JSON.stringify({banned: banned})
        })

        if (!response.ok) {
            return
        }
        
        this.getUsers()
    }

}   
</script>

<style scoped lang="scss">

</style>
