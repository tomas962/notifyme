<template>
    <div>
        

        <b-row class="mt-3">
            <b-col cols="8"><h1>Jūsų Paieškos</h1></b-col>
            <b-col>
                <b-button v-on:click="getFormData();" class="btn-info" v-b-modal.modal-1>Nauja paieška</b-button>
                <b-modal v-on:ok="okClicked()" ok-title="Išsaugoti" cancel-title="Atšaukti" id="modal-1" title="Nauja paieška" size="lg">
                    <b-form>
                        <b-row>
                            <b-col>
                                <b-form-select v-on:change="getModels();" v-model="newQuery.make_id" :options="queryFormData.makesOptions" ></b-form-select>
                            </b-col>
                            <b-col>
                                <b-form-select v-model="newQuery.model_id" :options="queryFormData.modelsOptions" ></b-form-select>
                            </b-col>
                        </b-row>
                        <b-row class="mt-3">
                            <b-col cols="6">
                                <b-form-group label="Kaina (€)">
                                    <b-row>
                                        <b-col cols="6">
                                            <b-form-input number="" v-model="newQuery.price_from" type="number" placeholder="Nuo"></b-form-input>
                                        </b-col>
                                        <b-col cols="6">
                                            <b-form-input  number="" v-model="newQuery.price_to" type="number" placeholder="Iki"></b-form-input>
                                        </b-col>
                                    </b-row>
                                </b-form-group>
                            </b-col>
                            <b-col cols="6">
                                <b-form-group label="Metai">
                                    <b-row>
                                        <b-col cols="6">
                                            <b-form-input number="" v-model="newQuery.year_from" type="number" placeholder="Nuo"></b-form-input>
                                        </b-col>
                                        <b-col cols="6">
                                            <b-form-input number="" v-model="newQuery.year_to" type="number" placeholder="Iki"></b-form-input>
                                        </b-col>
                                    </b-row>
                                </b-form-group>
                            </b-col>
                        </b-row>
                        <b-row>
                            <b-col>
                                <b-form-select v-model="newQuery.body_style_id" :options="queryFormData.bodyStyles" ></b-form-select>
                            </b-col>
                            <b-col>
                                <b-form-select v-model="newQuery.fuel_id" :options="queryFormData.fuelTypes" ></b-form-select>
                            </b-col>
                        </b-row>
                        <b-row >
                            <b-col cols="6" class="mt-3">
                                <b-form-select v-model="newQuery.city_id" :options="queryFormData.cities" ></b-form-select>
                                <b-form-input class="mt-3" v-model="newQuery.search_term" placeholder="Tekstinė paieška"></b-form-input>
                            </b-col>
                            <b-col cols="6" class="mt-3">
                                <b-form-group label="Tinklalapiai">
                                    <el-select placeholder="Tinklalapiai" 
                                    v-b-tooltip.hover title="Pasirinkite, kuriuose tinklalapiuose bus ieškomi skelbimai" 
                                    multiple v-model="newQuery.sites">
                                        <el-option class="autop-text" label="Autoplius" value="autoplius"></el-option>
                                        <el-option class="autob-text" label="Autobilis" value="autobilis"></el-option>
                                        <el-option class="autog-text" label="Autogidas" value="autogidas"></el-option>
                                    </el-select>
                                </b-form-group>
                            </b-col>
                        </b-row>
                        
                        <b-row class="mt-3">
                            <b-col>
                                <div>
                                <h4 id="more-params" v-on:click="formExpanded=!formExpanded" v-b-toggle.collapse-3 class="m-1 pb-1 border-bottom">
                                    <b-icon-arrow-down-short v-if="!formExpanded" scale="2"></b-icon-arrow-down-short> 
                                    <b-icon-arrow-up-short v-if="formExpanded" scale="2"></b-icon-arrow-up-short> 
                                    Daugiau parametrų</h4>
                                <b-collapse id="collapse-3">
                                    <b-row class="mt-3">
                                        <b-col cols="6">
                                            <b-form-group label="Galingumas (kW)">
                                                <b-row>
                                                    <b-col cols="6">
                                                        <b-form-input number="" v-model="newQuery.power_from" type="number" placeholder="Nuo"></b-form-input>
                                                    </b-col>
                                                    <b-col cols="6">
                                                        <b-form-input  number="" v-model="newQuery.power_to" type="number" placeholder="Iki"></b-form-input>
                                                    </b-col>
                                                </b-row>
                                            </b-form-group>
                                        </b-col>
                                    </b-row>
                                </b-collapse>
                                </div>
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
import {Select} from "element-ui"

interface SelectOption {
    value: string|number|null;
    text: string;
}

interface QueryFormData {
    makesOptions: SelectOption[];
    modelsOptions: SelectOption[];
    makes: Make[];
    bodyStyles: SelectOption[];
    fuelTypes: SelectOption[];
    cities: any[];
}

@Component({
    components: {
        CarQueryComp,
        Select
    }
})
export default class CarQueries extends Vue {
    formExpanded = false;
    queries: CarQueryResponse[] = []
    newQuery: NewCarQuery = {
        make_id: 1,
        model_id: null,
        city_id: null,
        power_from: null,
        power_to: null,
        search_term: "",
        year_to: null,
        year_from: null,
        body_style_id: null,
        fuel_id: null,
        price_from: null,
        price_to: null,
        sites: ["autogidas","autobilis","autoplius"]
    }

    queryFormData: QueryFormData = {
        makesOptions: [],
        modelsOptions: [{text:"Visi modeliai", value: null}],
        makes: [],
        bodyStyles: [{text:"Kėbulo tipas", value: null}],
        fuelTypes: [{text:"Kuro tipas", value: null}],
        cities: [{text: "Visi miestai", value: null}]
    }

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
            this.queryFormData.makes = data;
            this.queryFormData.makesOptions = this.queryFormData.makes.map((make) => {
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
        this.queryFormData.modelsOptions = [{text:"Visi modeliai", value: null}]
        this.queryFormData.modelsOptions = this.queryFormData.modelsOptions.concat(data.map((model: any) => {
            return {
                text: model.model_name,
                value: model.id
            }
        }));
        console.log(this.queryFormData.modelsOptions);
        
    }

    async getBodyStyles() {
        const response = await fetch(window.SERVER_URL + "/body_styles");
        const data = await response.json();
        this.queryFormData.bodyStyles = [{text:"Kėbulo tipas", value: null}]
        this.queryFormData.bodyStyles = this.queryFormData.bodyStyles.concat(data.map((body_style: any) => {
            return {
                value: body_style.id,
                text: body_style.name
            }
        }));
    }

    async getFuelTypes() {
        const response = await fetch(window.SERVER_URL + "/fuel_types");
        const data = await response.json();
        this.queryFormData.fuelTypes = [{text:"Kuro tipas", value: null}]
        this.queryFormData.fuelTypes = this.queryFormData.fuelTypes.concat(data.map((fuel_type: any) => {
            return {
                value: fuel_type.id,
                text: fuel_type.fuel_name
            }
        }));
    }

    async getCities() {
        const response = await fetch(window.SERVER_URL + "/cities");
        const data = await response.json();
        this.queryFormData.cities = [{text:"Visi miestai", value: null}]
        this.queryFormData.cities = this.queryFormData.cities.concat(data.map((city: any) => {
            return {
                value: city.id,
                text: city.city
            }
        }));

        this.queryFormData.cities = [
            {text:"Visi miestai", value: null},
            {
                label: "Didieji miestai",
                options: this.queryFormData.cities.slice(1,6)
                
            },
            {
                label: "Kiti miestai",
                options: this.queryFormData.cities.slice(6)
                
            }
        ]
    }

    async getFormData() {
        this.getMakes();
        this.getBodyStyles();
        this.getFuelTypes();
        this.getCities();
    }

    async okClicked() {
        console.log(JSON.stringify(this.newQuery));
        try {
            const response = await fetch(window.SERVER_URL + "/users/" + this.$store.state.User.identity.user_id + "/queries", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.newQuery)
        })
        
        } catch (error) {
            console.log(error);
            
        }

        
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.autog-text {
    color: #FEA638 !important; 
}

.autop-text {
    color: #1174b9 !important; 
}

.autob-text {
    color: #df1d38 !important; 
}

.modal-dialog {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}

.modal-content {
  height: auto;
  min-height: 100%;
  border-radius: 0;
}

#more-params:hover{
    color: blue;
    cursor: pointer;
}
</style>
