<template>
    <div>
        

        <b-row class="mt-3">
            <b-col cols="8"><h1>Jūsų Paieškos</h1></b-col>
            <b-col>
                <b-button v-on:click="getMakes();" class="btn-info" v-b-modal.modal-1>Nauja paieška</b-button>
                <b-modal id="modal-1" title="Nauja paieška">
                    <b-form>
                        <b-row>
                            <b-col>
                                <b-form-select v-on:change="getModels();" v-model="newQuery.make_id" :options="makesOptions" ></b-form-select>
                            </b-col>
                            <b-col>
                                <b-form-select v-model="newQuery.model_id" :options="modelsOptions" ></b-form-select>
                            </b-col>
                        </b-row>
                        <b-row>
                            <b-col>
                                <b-form-group></b-form-group>
                            </b-col>
                        </b-row>
                    </b-form>
                </b-modal>
            </b-col>
        </b-row>
        <CarQueryComp v-for="query in queries" :key="query.car_query.id" :query="query"></CarQueryComp>
    </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import {CarQueryResponse, NewCarQuery, Make} from "@/models/interfaces"
import CarQueryComp from "@/components/CarQuery.vue"

@Component({
    components: {
        CarQueryComp
    }
})
export default class CarQueries extends Vue {
    queries: CarQueryResponse[] = []
    newQuery: NewCarQuery = {
        make_id: 1,
        model_id: -1,
        city_id: 0,
        power_from: 0,
        power_to: 0,
        search_term: "",
        year_to: 0,
        year_from: 0,
        body_style_id: 0,
        fuel_id: 0,
        price_from: 0,
        price_to: 0
    }

    makes: Make[] = []

    makesOptions: any[] = []
    modelsOptions: any[] = [{text:"Visi modeliai", value: -1}]
    created() {
        console.log("CREATED");
        fetch(window.SERVER_URL + "/users/" + this.$store.state.User.identity.user_id + "/queries")
        .then((response) => response.json())
        .then((data: CarQueryResponse[]) => {
            console.log(data);
            this.queries = data
        })
    }

    async getMakes() {
        const response = await fetch(window.SERVER_URL + "/makes");
        if (response.ok) {
            const data: Make[] = await response.json();
            this.makes = data;
            this.makesOptions = this.makes.map((make) => {
                return {
                    text: make.make,
                    value: make.id
                }
            })
            
        }
    }

    async getModels() {
        const response = await fetch(window.SERVER_URL + "/makes/" + this.newQuery.make_id + "/models");
        const data = await response.json();
        this.modelsOptions = [{text:"Visi modeliai", value: -1}]
        this.modelsOptions = this.modelsOptions.concat(data.map((model: any) => {
            return {
                text: model.model_name,
                value: model.id
            }
        }));
        console.log(this.modelsOptions);
        
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
