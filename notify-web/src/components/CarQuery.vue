<template>
        <b-col class="rounded  pl-0 pt-2" xl="3"  sm="6">
                <b-card bg-variant="dark" :header="card_title" style="height: 100%;">
                    <b-card-text >
                        <ul class="pl-3" style="height: 100%">
                            <li v-if="query.car_query.city">
                                {{query.car_query.city}}
                            </li>
                            <li v-if="query.car_query.price_from !== null || query.car_query.price_to !== null">
                                {{priceText}}
                            </li>
                            <li v-if="query.car_query.year_from !== null || query.car_query.year_to !== null">
                                {{yearText}}
                            </li>
                        </ul>
                        <div class="mb-2" style="display: flex">
                            <div v-if="query.car_query.sites && query.car_query.sites.includes('autoplius')" style="height:20px; width:20px;" class="pl-1 site-cube autop rounded">P</div>
                            <div v-if="query.car_query.sites && query.car_query.sites.includes('autogidas')" style="height:20px; width:20px;" class="pl-1 site-cube autog rounded ml-1">G</div>
                            <div v-if="query.car_query.sites && query.car_query.sites.includes('autobilis')" style="height:20px; width:20px;" class="pl-1 site-cube autob rounded ml-1">B</div>
                        </div>
                    </b-card-text>
                    <template v-slot:footer>
                        <b-row>
                            <b-col v-if="identity.group == 'admin'" class="text-center mb-1" cols="12">
                                <b-btn :disabled="query.car_query.currently_scraping || nextScrape <= 0 ? true : false" 
                                class="btn-info" v-b-tooltip.hover title="Priverstinai pradėti paiešką" @click="requestQueryStart()">
                                    Pradėti paiešką
                                </b-btn>
                            </b-col>
                        </b-row>
                        <b-row>
                            <b-col class="text-center" cols="12">
                                <b-btn :disabled="query.car_query.currently_scraping ? true : false" @click="setPage({page: 1})" :to="'/users/'+$route.params.user_id+'/queries/' + query.car_query.id + '/cars'" class="btn-success">
                                    <b-spinner v-if="query.car_query.currently_scraping ? true : false" small></b-spinner>
                                    {{query.car_query.currently_scraping ? 'Paieška vykdoma' : 'Rezultatai'}}
                                </b-btn>
                            </b-col>
                        </b-row>
                        <b-row class="mt-2">
                            <b-col class="text-center">
                            <b-btn-group size="sm">
                                <b-button class="btn-danger" v-b-modal="'del-query'+query.car_query.id">Pašalinti</b-button>
                                <b-modal :id="'del-query'+query.car_query.id" title="Paieškos trynimas"
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
                        <b-row v-if="!query.car_query.currently_scraping">
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
import {CarQueryResponse} from "@/models/interfaces"

import {namespace} from 'vuex-class'
import {Identity} from '@/store/modules/user'
const UIns = namespace('UIState')
const userns = namespace('User')

@Component
export default class CarQueryComp extends Vue {
    @Prop() query!: CarQueryResponse
    showErr = false;
    errMsg: string|null = null;
    intervalID = 0

    @userns.State
    identity!: Identity;


    @UIns.Action
    setPage!: (state: {page: number}) => void

    destroyed() {
        clearInterval(this.intervalID)
    }

    created() {
        this._nextScrape();
        this.intervalID = setInterval(this._nextScrape, 1000);
    }

    get card_title() {
        if (this.query.make_model && this.query.make_model.make) 
            if (this.query.make_model.model_name)
                return this.query.make_model.make + " " + this.query.make_model.model_name
            else 
                return  this.query.make_model.make
        else 
            return "Visos markės"
    }
    get priceText() {
        if (this.query.car_query.price_from !== null && this.query.car_query.price_to !== null)
            return `Nuo ${this.query.car_query.price_from}€ iki ${this.query.car_query.price_to}€`
        if (this.query.car_query.price_from !== null)
            return `Nuo ${this.query.car_query.price_from}€`
        if (this.query.car_query.price_to !== null)
            return `Iki ${this.query.car_query.price_to}€`

        return ""
    }

    get yearText() {
        if (this.query.car_query.year_from !== null && this.query.car_query.year_to !== null)
            return `Nuo ${this.query.car_query.year_from} m. iki ${this.query.car_query.year_to} m.`
        if (this.query.car_query.year_from !== null)
            return `Nuo ${this.query.car_query.year_from} m.`
        if (this.query.car_query.year_to !== null)
            return `Iki ${this.query.car_query.year_to} m.`
        return ""
    }

    nextScrape = 0;
    _nextScrape() {
        const timestamp = (Date.now() / 1000) | 0;
        this.nextScrape = (this.query.car_query.last_scraped + (this.query.car_query.scrape_interval || window.SCRAPE_INTERVAL)) - timestamp
    }

    edit(){
        
        window.eventBus.$emit("query-edit", this.query)
        this.$bvModal.show("queryEditModal")
    }

    async delQuery() {
        console.log("deleting query:");
        console.log(this.query);
        
        const response = await fetch(window.SERVER_URL + "/users/" + this.$route.params.user_id + "/queries/" + this.query.car_query.id, {
            headers: {
                'Authorization': 'Bearer ' + this.$store.state.User.access_token
            },
            method: 'DELETE'
        })

        if (!response.ok) {
            this.errMsg = "Įvyko klaida ištrinant paiešką."
            this.showErr = true
        } else {
            window.eventBus.$emit('car-query-deleted')
        }
    }

    async requestQueryStart() {
        const response = await fetch(window.SERVER_URL + `/users/${this.$route.params.user_id}/queries/${this.query.car_query.id}/start`, {
            headers: {
                'Authorization': 'Bearer ' + this.$store.state.User.access_token
            },
            method: 'POST'
        })

        if (!response.ok) {
            this.errMsg = "Įvyko klaida pradedant paiešką."
            this.showErr = true
        } else {
            this.query.car_query.last_scraped = ((Date.now() / 1000) | 0) - window.SCRAPE_INTERVAL;
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