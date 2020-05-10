<template>
  <div>
      <h2 class="mt-3">Pranešimai</h2>
     <b-table :tbody-tr-attr="idAttr" bordered  hover :fields="[
        {key: 'Tema', thStyle:''},
        {key: 'Tekstas', thStyle:''},
        {key: 'Data', thStyle:'width: 10%'},
     ]" responsive class="mt-3" dark :items="tableMessages" ></b-table>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import {MessageResponse} from '@/models/interfaces'

@Component
export default class SettingsView extends Vue {
    messages: MessageResponse[] = []

    get tableMessages(){
        const msgs = this.messages.map((msg) => {
            return {
                "Tema": msg.title,
                "Tekstas": msg.text,
                "Data": new Date(msg.timestamp).toISOString().replace(/T/, " ").replace(/.000Z/, ""),
                "Id": msg.id
            }
        })
        return msgs
    }
    async created(){
        const response = await fetch(window.SERVER_URL + `/users/${this.$store.state.User.identity.user_id}/messages`, {
            headers: {
                'Authorization': 'Bearer ' + this.$store.state.User.access_token
            }
        })

        if (!response.ok){
            console.log("get messages error");
            return
        }

        const data: MessageResponse[] = await response.json()
        console.log("messages:");
        console.log(data);
        
        this.messages = data;
        //this.formatMessages();
    }

    formatMessages() {
        for (let i = 0; i < this.messages.length; i++) {
            const text = this.messages[i].text
        }
    }

    idAttr(item, row){
        console.log(item);
        return {test:item.id}
    }
}   
</script>

<style scoped lang="scss">

</style>
