<template>
    <div>
        

        <b-row class="mt-3">
            <b-col cols="8"><h1>Jūsų Paieškos</h1></b-col>
            <b-col>
                <b-button v-on:click="getFormData();" class="btn-info" v-b-modal.queryEditModal>Nauja paieška</b-button>
                <b-modal v-on:cancel="onCancelClick()" v-on:ok="okClicked()" ok-title="Išsaugoti" cancel-title="Atšaukti" id="queryEditModal" :title='editForm ? "Redaguojama paieška" : "Nauja paieška"' size="lg">
                    <b-form>
                        <b-row>
                            <b-col>
                                <b-form-select v-on:change="getModels(); log_('make changed')" v-model="newQuery.make_id" :options="queryFormData.makesOptions" ></b-form-select>
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
                                            <b-form-input number v-model="newQuery.price_from" type="number" placeholder="Nuo"></b-form-input>
                                        </b-col>
                                        <b-col cols="6">
                                            <b-form-input  number v-model="newQuery.price_to" type="number" placeholder="Iki"></b-form-input>
                                        </b-col>
                                    </b-row>
                                </b-form-group>
                            </b-col>
                            <b-col cols="6">
                                <b-form-group label="Metai">
                                    <b-row>
                                        <b-col cols="6">
                                            <b-form-input number v-model="newQuery.year_from" type="number" placeholder="Nuo"></b-form-input>
                                        </b-col>
                                        <b-col cols="6">
                                            <b-form-input number v-model="newQuery.year_to" type="number" placeholder="Iki"></b-form-input>
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
                                                        <b-form-input number="" v-model.number="newQuery.power_from" type="number" placeholder="Nuo"></b-form-input>
                                                    </b-col>
                                                    <b-col cols="6">
                                                        <b-form-input  number="" v-model.number="newQuery.power_to" type="number" placeholder="Iki"></b-form-input>
                                                    </b-col>
                                                </b-row>
                                            </b-form-group>
                                        </b-col>
                                        <b-col style="margin-top: 2rem">
                                            <b-form-select v-model="newQuery.gearbox" :options='[
                                                {value:null, text:"Pavarų dėžė"}, "Automatinė", "Mechaninė"
                                            ]' ></b-form-select>
                                        </b-col>
                                    </b-row>
                                    <b-row>
                                        <b-col>
                                            <b-form-select v-model="newQuery.driven_wheels" :options="[
                                            {value:null, text:'Varomieji ratai'},
                                            'Priekiniai varantys ratai',
                                            'Galiniai varantys ratai',
                                            'Visi varantys ratai']" ></b-form-select>
                                        </b-col>
                                        <b-col>
                                            <b-form-select v-model="newQuery.steering_column" :options="[
                                            {value:null, text:'Vairo padėtis'}, 
                                            'Kairėje','Dešinėje']" ></b-form-select>
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
        <b-row>
            <b-col class="ml-3" cols="12">
                <div class="font-italic">Tinklalapiai, kuriuose bus ieškomi skelbimai:</div>
                <div style="display: flex;">
                    <div style="height:20px; width:20px;" class="pl-1 mr-1 site-cube autop rounded">P</div> - Autoplius
                </div>
                <div style="display: flex;" class="mt-1">
                    <div style="height:20px; width:20px;" class="pl-1 mr-1 site-cube autog rounded">G</div> - Autogidas
                </div>
                <div style="display: flex;" class="mt-1">
                    <div style="height:20px; width:20px;" class="pl-1 mr-1 site-cube autob rounded">B</div> - Autobilis
                </div>
            </b-col>
        </b-row>
        <CarQueryRow v-for="query in queriesBy4" :key="query.reduce((acc, el) => acc * el.car_query.id, 1)" :queries4="query"></CarQueryRow>
    </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import {CarQueryResponse, NewCarQuery, Make} from "@/models/interfaces"
import CarQueryRow from "@/components/CarQueriesRow.vue"
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
        CarQueryRow,
        Select
    }
})
export default class CarQueries extends Vue {
    formExpanded = false;
    editForm = false;

    intervalID = 0;
    queriesBy4: CarQueryResponse[][] = []
    queries: CarQueryResponse[] = []
    newQuery: NewCarQuery = {
        make_id: 1,
        model_id: null,
        city_id: null,
        power_from: null,
        power_to: null,
        search_term: null,
        year_to: null,
        year_from: null,
        body_style_id: null,
        fuel_id: null,
        price_from: null,
        price_to: null,
        sites: ["autogidas","autobilis","autoplius"],
        query_id: null,
        gearbox: null,
        driven_wheels: null,
        steering_column: null
    }

    queryFormData: QueryFormData = {
        makesOptions: [],
        modelsOptions: [],
        makes: [],
        bodyStyles: [],
        fuelTypes: [],
        cities: []
    }

    log_(msg: string) {
        console.log(msg);
        
    }

    @Watch('queries')
    onQueriesChanged(newQueries: CarQueryResponse[]) {  
        const tmp: CarQueryResponse[][] = []
        for (let i = 0; i < newQueries.length; i+=4) {
            const row: CarQueryResponse[] = []
            row.push(newQueries[i])
            if (newQueries.length > i+1)
                row.push(newQueries[i+1])
            if (newQueries.length > i+2)
                row.push(newQueries[i+2])
            if (newQueries.length > i+3)
                row.push(newQueries[i+3])
            tmp.push(row)
        }
        console.log("QUERIES CHANGED");
        
        this.queriesBy4 = tmp;
    }

    async getQueries() {
        const response = await fetch(window.SERVER_URL + "/users/" + this.$store.state.User.identity.user_id + "/queries", {
            headers: {
                'Authorization': 'Bearer ' + this.$store.state.User.access_token
            }
        });
        const data: CarQueryResponse[] = await response.json();
        this.queries = data
        
    }

    async getModels() {
        const response = await fetch(window.SERVER_URL + "/makes/" + this.newQuery.make_id + "/models",  {
            headers: {
                'Authorization': 'Bearer ' + this.$store.state.User.access_token
            }
        });
        const data = await response.json();
        this.queryFormData.modelsOptions = [{text:"Visi modeliai", value: null}]
        this.queryFormData.modelsOptions = this.queryFormData.modelsOptions.concat(data.map((model: any) => {
            return {
                text: model.model_name,
                value: model.id
            }
        }));
        
    }

    beforeDestroy() {
        window.eventBus.$off('query-edit')
        window.eventBus.$off('car-query-deleted')
        window.socket.off('car_query_started')
        window.socket.off('car_query_ended')
        clearInterval(this.intervalID)
    }

    created() {
        this.getQueries();
        window.socket.on('car_query_started', (data: {user_id: number; query_id: number}) => {
            console.log('query started:');
            console.log(data);
            const q = this.queries.find((query) => 
                query.car_query.user_id == data.user_id && query.car_query.id == data.query_id
            )
            if (q)
                q.car_query.currently_scraping = 1
        })

        window.socket.on('car_query_ended', (data: {user_id: number; query_id: number}) => {
            console.log('query ended:');
            console.log(data);
            const q = this.queries.find((query) => 
                query.car_query.user_id == data.user_id && query.car_query.id == data.query_id
            )
            if (q){
                q.car_query.currently_scraping = 0
                q.car_query.last_scraped = (Date.now() / 1000) | 0;
            }
        })
        
        window.eventBus.$on("query-edit", async (query: CarQueryResponse) => {
            console.log("ON QUERY-EDIT EMMITED");
            
            this.editForm = true;
            this.newQuery.make_id = (query.make_model !== null && query.make_model.make_id !== null) ? query.make_model.make_id : 1
            this.newQuery.model_id = query.make_model ? query.make_model.model_id : null
            this.newQuery.price_from = query.car_query.price_from
            this.newQuery.price_to = query.car_query.price_to
            this.newQuery.sites = query.car_query.sites ? query.car_query.sites.split(',') : []
            this.newQuery.city_id = query.car_query.city_id
            this.newQuery.power_from = query.car_query.power_from
            this.newQuery.power_to = query.car_query.power_to  
            this.newQuery.search_term = query.car_query.search_term
            this.newQuery.year_to = query.car_query.year_to
            this.newQuery.year_from = query.car_query.year_from
            this.newQuery.body_style_id = query.body_style ? query.body_style.id : null
            this.newQuery.query_id = query.car_query.id
            this.newQuery.fuel_id = query.fuel_type ? query.fuel_type.id : null
            this.newQuery.gearbox = query.car_query ? query.car_query.gearbox : null
            this.newQuery.driven_wheels = query.car_query ? query.car_query.driven_wheels : null
            this.newQuery.steering_column = query.car_query ? query.car_query.steering_column : null
            this.getFormData();
            this.getModels();
        })

        window.eventBus.$on('car-query-deleted', () => {
            console.log("car query delted");
            this.getQueries();
        })
    
    }

    async getMakes() {
        const response = await fetch(window.SERVER_URL + "/makes",  {
            headers: {
                'Authorization': 'Bearer ' + this.$store.state.User.access_token
            }
        });
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


    async getBodyStyles() {
        const response = await fetch(window.SERVER_URL + "/body_styles", {
            headers: {
                'Authorization': 'Bearer ' + this.$store.state.User.access_token
            }
        });
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
        const response = await fetch(window.SERVER_URL + "/fuel_types", {
            headers: {
                'Authorization': 'Bearer ' + this.$store.state.User.access_token
            }
        });
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
        const response = await fetch(window.SERVER_URL + "/cities", {
            headers: {
                'Authorization': 'Bearer ' + this.$store.state.User.access_token
            }
        });
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
        if (this.queryFormData.makesOptions.length === 0)
            this.getMakes();
        if (this.queryFormData.bodyStyles.length === 0)
            this.getBodyStyles();
        if (this.queryFormData.fuelTypes.length === 0)
            this.getFuelTypes();
        if (this.queryFormData.cities.length === 0)
            this.getCities();
    }

    async okClicked() {
        console.log("BEFORE:");
        console.log(this.newQuery);
        
        for (const key in this.newQuery) {
            this.newQuery[key] = typeof this.newQuery[key] === "string"  && this.newQuery[key].length == 0 ? null :  this.newQuery[key];
        }
        console.log("AFTER:");
        console.log(this.newQuery);
        if (this.newQuery.query_id === null){ //add new
            const response = await fetch(window.SERVER_URL + "/users/" + this.$store.state.User.identity.user_id + "/queries", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + this.$store.state.User.access_token
                },
                body: JSON.stringify(this.newQuery)
            })
        }
        else { //update existing
            const response = await fetch(window.SERVER_URL + "/users/" + this.$store.state.User.identity.user_id + "/queries/" + this.newQuery.query_id, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + this.$store.state.User.access_token
                },
                body: JSON.stringify(this.newQuery)
            })

        }
        this.getQueries();
        this.newQuery = this.defaultQueryValues()
    }

    defaultQueryValues(): NewCarQuery {
        return { //reset values
            make_id: 1,
            model_id: null,
            city_id: null,
            power_from: null,
            power_to: null,
            search_term: null,
            year_to: null,
            year_from: null,
            body_style_id: null,
            fuel_id: null,
            price_from: null,
            price_to: null,
            sites: ["autogidas","autobilis","autoplius"],
            query_id: null,
            gearbox: null,
            driven_wheels: null,
            steering_column: null
        }
    }

    onCancelClick() {
        this.editForm = false;
        this.newQuery = this.defaultQueryValues()
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss">
.autog-text {
    color: #FEA638 !important; 
}

.autop-text {
    color: #1174b9 !important; 
}

.autob-text {
    color: #df1d38 !important; 
}

// .modal-dialog {
//   width: 100%;
//   height: 100%;
//   margin: 0;
//   padding: 0;
// }

// .modal-content {
//   height: auto;
//   min-height: 100%;
//   border-radius: 0;
// }

#more-params:hover{
    color: blue;
    cursor: pointer;
}
</style>
