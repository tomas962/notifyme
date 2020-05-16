<template>
        <b-col class="rounded  pl-0 pt-2" xl="3"  sm="6">
                <b-card bg-variant="dark" :header="card_title" style="height: 100%;">
                    <b-card-text >
                        <ul class="pl-3" style="height: 100%">
                            <li v-if="query.price_from !== null || query.price_to !== null">
                                {{priceText}}
                            </li>
                            <li v-if="query.year_from !== null || query.year_to !== null">
                                {{yearText}}
                            </li>
                        </ul>
                        <div class="mb-2" style="display: flex">
                            <div v-if="query.sites && query.sites.includes('domo')" style="height:20px; width:20px;" class="pl-1 site-cube domo-bg rounded">D</div>
                            <div v-if="query.sites && query.sites.includes('skelbiu')" style="height:20px; width:20px;" class="pl-1 site-cube skelbiu-bg rounded ml-1">S</div>
                        </div>
                    </b-card-text>
                    <template v-slot:footer>
                        <b-row>
                            <b-col v-if="identity.group == 'admin'" class="text-center mb-1" cols="12">
                                <b-btn :disabled="query.currently_scraping || nextScrape <= 0 ? true : false" 
                                class="btn-info" v-b-tooltip.hover title="Priverstinai pradėti paiešką" @click="requestQueryStart()">
                                    Pradėti paiešką
                                </b-btn>
                            </b-col>
                        </b-row>
                        <b-row>
                            <b-col class="text-center" cols="12">
                                <b-btn :disabled="query.currently_scraping ? true : false" @click="; /*setPage({page: 1})*/" :to="'/users/'+identity.user_id+'/re_queries/' + query.id + '/re_ads'" class="btn-success">
                                    <b-spinner v-if="query.currently_scraping ? true : false" small></b-spinner>
                                    {{query.currently_scraping ? 'Paieška vykdoma' : 'Rezultatai'}}
                                </b-btn>
                            </b-col>
                        </b-row>
                        <b-row class="mt-2">
                            <b-col class="text-center">
                            <b-btn-group size="sm">
                                <b-button class="btn-danger" v-b-modal="'del-query'+query.id">Pašalinti</b-button>
                                <b-modal :id="'del-query'+query.id" title="Paieškos trynimas"
                                ok-title="Ištrinti" cancel-title="Atšaukti" v-on:ok="delQuery()" ok-variant="danger">
                                    <p>
                                        Ar tikrai norite ištrinti šią paiešką? (<strong>{{card_title}}</strong>)
                                    </p>
                                    <strong class="font-italic">Bus ištrinti visi šios paieškos rezultatai!</strong>
                                </b-modal>
                                <b-btn v-on:click="edit();">Redaguoti</b-btn>
                            </b-btn-group>
                            </b-col>
                        </b-row>
                        <b-alert class="mt-2" variant="danger" :show="showErr" dismissible v-on:dismissed="showErr=false">{{errMsg}}</b-alert>
                        <b-row v-if="!query.currently_scraping">
                            <b-col v-if="nextScrape > 0">
                                Bus atnaujinama už: {{Math.floor(nextScrape/60)}}min {{nextScrape%60}}s
                            </b-col>
                            <b-col v-else>
                                Paieška laukia eilėje
                            </b-col>
                        </b-row>
                    </template>
                </b-card>
        </b-col>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import {ReQueryResponse} from "@/models/interfaces"

import {namespace} from 'vuex-class'
import {Identity} from '@/store/modules/user'
const UIns = namespace('UIState')
const userns = namespace('User')

@Component
export default class ReQueryComp extends Vue {
    @Prop() query!: ReQueryResponse
    showErr = false;
    errMsg: string|null = null;
    intervalID = 0

    @userns.State
    identity!: Identity;


    // @UIns.Action
    // setPage!: (state: {page: number}) => void

    destroyed() {
        clearInterval(this.intervalID)
    }

    created() {
        if (!this.query.last_scraped) {
            this.query.last_scraped = (Date.now() / 1000) | 0;
        }
        this._nextScrape();
        this.intervalID = setInterval(this._nextScrape, 1000);
    }

    get card_title() {
        if (this.query.category_name && this.query.city)
            return `${this.query.category_name}, ${this.query.city}`
        if (this.query.category_name)
            return `${this.query.category_name}, Visi miestai`
        if (this.query.city)
            return `Visos kategorijos, ${this.query.city}`
        
            return "Visos kategorijos, Visi miestai"
    }
    get priceText() {
        if (this.query.price_from !== null && this.query.price_to !== null)
            return `Nuo ${this.query.price_from}€ iki ${this.query.price_to}€`
        if (this.query.price_from !== null)
            return `Nuo ${this.query.price_from}€`
        if (this.query.price_to !== null)
            return `Iki ${this.query.price_to}€`

        return ""
    }

    get yearText() {
        if (this.query.year_from !== null && this.query.year_to !== null)
            return `Nuo ${this.query.year_from} m. iki ${this.query.year_to} m.`
        if (this.query.year_from !== null)
            return `Nuo ${this.query.year_from} m.`
        if (this.query.year_to !== null)
            return `Iki ${this.query.year_to} m.`
        return ""
    }

    nextScrape = 0;
    _nextScrape() {
        const timestamp = (Date.now() / 1000) | 0;
        this.nextScrape = this.query.last_scraped! + (this.query.scrape_interval || window.SCRAPE_INTERVAL) - timestamp
    }

    edit(){
        window.eventBus.$emit("re-query-edit", this.query)
        this.$bvModal.show("reQueryEditModal")
    }

    async delQuery() {
        console.log("deleting re query:");
        console.log(this.query);
        
        const response = await fetch(window.SERVER_URL + "/users/" + this.$store.state.User.identity.user_id + "/re_queries/" + this.query.id, {
            headers: {
                'Authorization': 'Bearer ' + this.$store.state.User.access_token
            },
            method: 'DELETE'
        })

        if (!response.ok) {
            this.errMsg = "Įvyko klaida ištrinant paiešką."
            this.showErr = true
        } else {
            console.log("emmiting re=query-deleted");
            
            window.eventBus.$emit('re-query-deleted')
        }
    }

    async requestQueryStart() {
        const response = await fetch(window.SERVER_URL + `/users/${this.$store.state.User.identity.user_id}/re_queries/${this.query.id}/start`, {
            headers: {
                'Authorization': 'Bearer ' + this.$store.state.User.access_token
            },
            method: 'POST'
        })

        if (!response.ok) {
            this.errMsg = "Įvyko klaida pradedant paiešką."
            this.showErr = true
        } else {
            this.query.last_scraped = ((Date.now() / 1000) | 0) - window.SCRAPE_INTERVAL;
        }

    }
}
</script>

<style lang="scss" scoped>
    .neg-pd {
        padding-left: -30px !important;
        width: 10px;
    }

</style>