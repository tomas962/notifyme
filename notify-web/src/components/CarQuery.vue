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
                            <b-col cols="6">
                                <b-btn v-on:click="edit();">Redaguoti</b-btn>
                            </b-col>
                            <b-col cols="6">
                                <router-link :to="'/queries/' + query.car_query.id + '/cars'">
                                    <b-btn class="btn-success">Rezultatai</b-btn>
                                </router-link>
                            </b-col>
                        </b-row>
                    </template>
                </b-card>
        </b-col>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import {CarQueryResponse} from "@/models/interfaces"

@Component
export default class CarQueryComp extends Vue {
    @Prop() query!: CarQueryResponse

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


    edit(){
        
        this.$root.$emit("query-edit", this.query)
        this.$bvModal.show("queryEditModal")
    }
}
</script>

<style lang="scss" scoped>
    .neg-pd {
        padding-left: -30px !important;
        width: 10px;
    }

</style>