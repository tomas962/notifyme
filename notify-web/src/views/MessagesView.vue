<template>
  <div>
      <h2 class="mt-3">Pranešimai</h2>
    <div class="overflow-auto">
        <b-pagination
        v-model="currentPage"
        :total-rows="tableMessages.length"
        :per-page="perPage"
        aria-controls="msg-table"
        ></b-pagination>
        <b-table id="msg-table" bordered  hover :fields="[
            {key: 'Tema', thStyle:''},
            {key: 'Tekstas', thStyle:''},
            {key: 'Data', thStyle:'width: 10%'},
        ]" 
        :per-page="perPage"
        :current-page="currentPage"
        responsive class="mt-3" dark :items="tableMessages" >
        
            <template v-slot:cell(Tekstas)="data">
                <div v-for="line in data.value.split('\n')" :key="line">
                    {{line}}
                    <a :href="formatLine(line)">{{formatLine(line) ? "nuoroda" : ""}}</a>
                </div>
            </template>

        </b-table>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import {MessageResponse} from '@/models/interfaces'

@Component
export default class SettingsView extends Vue {
    messages: MessageResponse[] = []
    currentPage = 1
    perPage = 10

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
        
        this.messages = data.reverse();
        //this.formatMessages();
    }

    formatMessages() {
        for (let i = 0; i < this.messages.length; i++) {
            const text = this.messages[i].text
        }
    }

    idAttr(item: any, row: any){
        console.log(item);
        return {test:item.id}
    }

    formatLine(line: string) {
        console.log(line.match(/https?:\/\/w?w?w?\.?notifyme\.ml\S*/));
        const link = line.match(/https?:\/\/w?w?w?\.?notifyme\.ml\S*/)
        if(link)
            return link[0]
        return ""
    }
}   
</script>

<style scoped lang="scss">

</style>
