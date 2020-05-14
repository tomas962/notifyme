<template>
<div>
    <b-row class="text-center mt-2">
        <b-col>
            <b-pagination 
            v-model="currentPage"
            :total-rows="re_ads.length"
            :per-page="perPage"
            align="center"
            ></b-pagination>
        </b-col>
    </b-row>
    
    <ReAdComp v-for="ad in adPage" :key="ad.id" :re_ad="ad" />
</div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import ReAdComp from '@/components/ReAd.vue'
import {namespace} from 'vuex-class'
import {ReAd} from '@/models/interfaces'

const UI = namespace('UIState')

@Component({
components: {
    ReAdComp
}
})
export default class ReAdList extends Vue {
    query_id = -1;
    user_id = 0;

    perPage = 10;

    re_ads: ReAd[] = []
    get currentPage () {
        return this.carAdsPage
    }
    set currentPage(val) {
        this.setPage({
            page: val
        });
    }

    @UI.State
    carAdsPage!: number;
    @UI.Action
    setPage!: (state: {page: number}) => void

    created() {
        console.log("ReAdList created");
        
        if (this.currentPage == null) {
            this.currentPage = 1
        }
        this.query_id = parseInt(this.$route.params.query_id, 10);
        this.user_id = parseInt(this.$route.params.user_id, 10);
        this.getReAds()
        console.log("_currentPage:");
        console.log(this.currentPage);
        
    }

    async getReAds() {
        const response = await fetch(window.SERVER_URL + `/users/${this.user_id}/re_queries/${this.query_id}/re_ads`, {
            headers: {
                'Authorization': 'Bearer ' + this.$store.state.User.access_token
            }
        })

        const data: ReAd[] = await response.json();
        console.log(data);
        this.re_ads = data.reverse();
    }

    get adPage() {
        const start = (this.currentPage-1) * this.perPage
        const end = start + this.perPage
        console.log(start);
        console.log(end);
        
        return this.re_ads.slice(start, end);
    }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>
