<template>
    <div>
        
        <b-alert class="mt-2" variant="danger" :show="showErr" dismissible v-on:dismissed="showErr=false">{{errMsg}}</b-alert>
        <b-row class="mt-3">
            <b-col cols="8"><h2>Jūsų Paieškos - Nekilnojamasis turtas</h2></b-col>
            <b-col>
                <b-button v-on:click="getFormData();" class="btn-info" v-b-modal.reQueryEditModal>Nauja paieška</b-button>
                <b-modal v-on:cancel="onCancelClick()" v-on:ok="okClicked()" ok-title="Išsaugoti" cancel-title="Atšaukti" id="reQueryEditModal" :title='editForm ? "Redaguojama paieška" : "Nauja paieška"' size="lg">
                    <b-form>
                        <b-row>
                            <b-col>
                                <b-form-select v-model="newQuery.category_id" :options="queryFormData.categories" ></b-form-select>
                            </b-col>
                            <b-col>
                                <b-form-select v-model="newQuery.city_id" :options="queryFormData.cities" ></b-form-select>
                            </b-col>
                        </b-row>
                        <b-row class="mt-3">
                            <b-col cols="6">
                                <b-form-group label="Kaina (€)">
                                    <b-row>
                                        <b-col cols="6">
                                            <b-form-input number v-model.number="newQuery.price_from" type="number" placeholder="Nuo"></b-form-input>
                                        </b-col>
                                        <b-col cols="6">
                                            <b-form-input  number v-model.number="newQuery.price_to" type="number" placeholder="Iki"></b-form-input>
                                        </b-col>
                                    </b-row>
                                </b-form-group>
                                <b-form-input class="mt-3" v-model="newQuery.search_term" placeholder="Tekstinė paieška"></b-form-input>
                            </b-col>
                            <b-col cols="6">
                                <b-form-group label="Plotas, m²">
                                    <b-row>
                                        <b-col cols="6">
                                            <b-form-input number v-model.number="newQuery.area_from" type="number" placeholder="Nuo"></b-form-input>
                                        </b-col>
                                        <b-col cols="6">
                                            <b-form-input number v-model.number="newQuery.area_to" type="number" placeholder="Iki"></b-form-input>
                                        </b-col>
                                    </b-row>
                                </b-form-group>
                                <b-col cols="6" class="mt-3">
                                <b-form-group label="Tinklalapiai">
                                    <el-select placeholder="Tinklalapiai" 
                                    v-b-tooltip.hover title="Pasirinkite, kuriuose tinklalapiuose bus ieškomi skelbimai" 
                                    multiple v-model="newQuery.sites">
                                        <el-option class="domo-text" label="Domoplius.lt" value="domoplius.lt"></el-option>
                                        <el-option class="skelbiu-text" label="Skelbiu.lt" value="skelbiu.lt"></el-option>
                                    </el-select>
                                </b-form-group>
                            </b-col>
                            </b-col>
                        </b-row>
                        <b-row class="mt-3">          
                            <b-col>
                                <div v-if="newQuery.category_id!=3">
                                <h4 id="more-params" v-on:click="formExpanded=!formExpanded" v-b-toggle.collapse-3 class="m-1 pb-1 border-bottom">
                                    <b-icon-arrow-down-short v-if="!formExpanded" scale="2"></b-icon-arrow-down-short> 
                                    <b-icon-arrow-up-short v-if="formExpanded" scale="2"></b-icon-arrow-up-short> 
                                    Išsami paieška</h4>
                                <b-collapse id="collapse-3">
                                    <b-row class="mt-3">
                                        <b-col cols="6">
                                            <b-form-group label="Kambarių skaičius">
                                                <b-row>
                                                    <b-col cols="6">
                                                        <b-form-input number v-model.number="newQuery.rooms_from" type="number" placeholder="Nuo"></b-form-input>
                                                    </b-col>
                                                    <b-col cols="6">
                                                        <b-form-input  number v-model.number="newQuery.rooms_to" type="number" placeholder="Iki"></b-form-input>
                                                    </b-col>
                                                </b-row>
                                            </b-form-group>
                                        </b-col>
                                        <b-col v-if="newQuery.category_id!=3" cols="6">
                                            <b-form-group label="Statybos metai">
                                                <b-row>
                                                    <b-col cols="6">
                                                        <b-form-input number v-model.number="newQuery.year_from" type="number" placeholder="Nuo"></b-form-input>
                                                    </b-col>
                                                    <b-col cols="6">
                                                        <b-form-input number v-model.number="newQuery.year_to" type="number" placeholder="Iki"></b-form-input>
                                                    </b-col>
                                                </b-row>
                                            </b-form-group>
                                        </b-col>
                                    </b-row>
                                    <b-row class="mt-3">
                                        <b-col cols="6">
                                            <b-form-select v-if="newQuery.category_id==2" v-model="newQuery.house_type_id" :options="queryFormData.reHouseTypes"></b-form-select>
                                        </b-col>
                                        <b-col cols="6">
                                            <b-form-select v-model="newQuery.type_id" :options="queryFormData.reTypes"></b-form-select>
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
                    <div style="height:20px; width:20px;" class="pl-1 mr-1 site-cube domo-bg rounded">D</div> - Domoplius.lt
                </div>
                <div style="display: flex;" class="mt-1">
                    <div style="height:20px; width:20px;" class="pl-1 mr-1 site-cube skelbiu-bg rounded">S</div> - Skelbiu.lt
                </div>
            </b-col>
        </b-row>
        <ReQueryRow v-for="query in queriesBy4" :key="query.reduce((acc, el) => acc * el.id, 1)" :queries4="query"></ReQueryRow>
    </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import {SelectOption, ReQueryResponse} from "@/models/interfaces"
import ReQueryRow from '@/components/ReQueriesRow.vue'

interface ReQueryDtata {
    cities: SelectOption[];
    categories: SelectOption[];
    reTypes: SelectOption[];
    reHouseTypes: SelectOption[];
}

interface ReCity {
    id: number;
    city: string;
}

interface ReCategory {
    id: number;
    name: string;
}

interface ReType {
    id: number;
    name: string;
}
interface ReHouseType {
    id: number;
    name: string;
}

interface ReQuery {
    [key: string]: any;
    city_id: number|null;
    category_id: number|null;
    price_from: number|null;
    price_to: number|null;
    year_from: number|null;
    year_to: number|null;
    area_from: number|null;
    area_to: number|null;
    type_id: number|null;
    rooms_from: number|null;
    rooms_to: number|null;
    search_term: string|null;
    house_type_id: number|null;
    sites: string[];
    query_id: number|null;
}

@Component({
    components:{
        ReQueryRow
    }
})
export default class REQueries extends Vue {
    showErr = false
    errMsg = ""

    newQuery: ReQuery = {
        city_id: null,
        category_id: null,
        price_from: null,
        price_to: null,
        year_from: null,
        year_to: null,
        area_from: null,
        area_to: null,
        type_id: null,
        rooms_from: null,
        rooms_to: null,
        search_term: null,
        house_type_id: null,
        sites: ["domoplius.lt", "skelbiu.lt"],
        query_id: null
    }
    queryFormData: ReQueryDtata = {
        cities: [],
        categories: [],
        reTypes: [],
        reHouseTypes: []
    }
    editForm = false
    formExpanded = false

    queriesBy4: ReQueryResponse[][] = []
    queries: ReQueryResponse[] = []

    beforeDestroy() {
        window.eventBus.$off('re-query-edit')
        window.eventBus.$off('re-query-deleted')
        window.socket.off('re_query_started')
        window.socket.off('re_query_ended')
    }

    created(){
        console.log("requeries created");
        this.getQueries();

        window.socket.on('re_query_started', (data: {user_id: number; query_id: number}) => {
            console.log('re query started:');
            console.log(data);
            const q = this.queries.find((query) => 
                query.user_id == data.user_id && query.id == data.query_id
            )
            if (q)
                q.currently_scraping = 1
        })

        window.socket.on('re_query_ended', (data: {user_id: number; query_id: number}) => {
            console.log('re query ended:');
            console.log(data);
            const q = this.queries.find((query) => 
                query.user_id == data.user_id && query.id == data.query_id
            )
            console.log(q);
            
            if (q){
                console.log("setting currently_scraping = 0");
                
                q.currently_scraping = 0
                q.last_scraped = (Date.now() / 1000) | 0;
            }
        })

        window.eventBus.$on('re-query-deleted', () => {
            console.log("re query delted");
            this.getQueries();
        })

        window.eventBus.$on("re-query-edit", async (query: ReQueryResponse) => {
            console.log("ON RE-QUERY-EDIT EMMITED");
            
            this.editForm = true;
            this.newQuery.city_id = query.city_id
            this.newQuery.category_id = query.category_id
            this.newQuery.rooms_to = query.rooms_to
            this.newQuery.rooms_from = query.rooms_from
            this.newQuery.search_term = query.search_term
            this.newQuery.house_type_id = query.house_type_id
            this.newQuery.sites = query.sites ? query.sites.split(',') : []
            this.newQuery.query_id = query.id
            this.newQuery.price_from = query.price_from
            this.newQuery.price_to = query.price_to
            this.newQuery.year_from = query.year_from
            this.newQuery.year_to = query.year_to
            this.newQuery.area_from = query.area_from
            this.newQuery.area_to = query.area_to
            this.newQuery.type_id = query.type_id
            this.newQuery.rooms_from = query.rooms_from

            this.getFormData();
        })
    }

    @Watch('queries')
    onQueriesChanged(newQueries: ReQueryResponse[]) {  
        const tmp: ReQueryResponse[][] = []
        for (let i = 0; i < newQueries.length; i+=4) {
            const row: ReQueryResponse[] = []
            row.push(newQueries[i])
            if (newQueries.length > i+1)
                row.push(newQueries[i+1])
            if (newQueries.length > i+2)
                row.push(newQueries[i+2])
            if (newQueries.length > i+3)
                row.push(newQueries[i+3])
            tmp.push(row)
        }
        console.log("RE QUERIES CHANGED");
        
        this.queriesBy4 = tmp;
    }

    async getCities(){
        if (this.queryFormData.cities.length !== 0)
            return
        const response =  await fetch(window.SERVER_URL + '/re_cities', {
            headers: {
                'Authorization': 'Bearer ' + this.$store.state.User.access_token
            }
        });

        if(!response.ok)
            return

        const data: ReCity[] = await response.json();
        this.queryFormData.cities = [{text:"Visi miestai", value:null}]
        this.queryFormData.cities = this.queryFormData.cities.concat(data.map((val) => {
            return {
                value: val.id,
                text:  val.city
            }
        }))
    }

    async getCategories() {
        if (this.queryFormData.categories.length !== 0)
            return
        const response =  await fetch(window.SERVER_URL + '/re_categories', {
            headers: {
                'Authorization': 'Bearer ' + this.$store.state.User.access_token
            }
        });

        if(!response.ok)
            return

        const data: ReCategory[] = await response.json();
        this.queryFormData.categories = [{text:"Visos kategorijos", value:null}]
        this.queryFormData.categories = this.queryFormData.categories.concat(data.map((val) => {
            return {
                value: val.id,
                text:  val.name
            }
        }))
    }

    async getReTypes() {
        if (this.queryFormData.reTypes.length !== 0)
            return
        const response = await fetch(window.SERVER_URL + '/re_types', {
            headers: {
                'Authorization': 'Bearer ' + this.$store.state.User.access_token
            }
        });

        if(!response.ok)
            return

        const data: ReType[] = await response.json();
        this.queryFormData.reTypes = [{text:"Namo tipas", value:null}]
        this.queryFormData.reTypes = this.queryFormData.reTypes.concat(data.map((val) => {
            return {
                value: val.id,
                text:  val.name
            }
        }))
    }

    async getReHouseTypes() {
        if (this.queryFormData.reHouseTypes.length !== 0)
            return
        const response = await fetch(window.SERVER_URL + '/re_house_types', {
            headers: {
                'Authorization': 'Bearer ' + this.$store.state.User.access_token
            }
        });

        if(!response.ok)
            return

        const data: ReHouseType[] = await response.json();
        this.queryFormData.reHouseTypes = [{text:"Pastato tipas", value:null}]
        this.queryFormData.reHouseTypes = this.queryFormData.reHouseTypes.concat(data.map((val) => {
            return {
                value: val.id,
                text:  val.name
            }
        }))
    }

    getFormData(){
        console.log();
        this.getCities();
        this.getCategories();
        this.getReTypes();
        this.getReHouseTypes();
    }
    onCancelClick() {
        this.editForm = false;
        this.newQuery = this.defaultQueryValues()
    }

    defaultQueryValues() {
        return {
            city_id: null,
            category_id: null,
            price_from: null,
            price_to: null,
            year_from: null,
            year_to: null,
            area_from: null,
            area_to: null,
            type_id: null,
            rooms_from: null,
            rooms_to: null,
            search_term: null,
            house_type_id: null,
            sites: ["domoplius.lt", "skelbiu.lt"],
            query_id: null,
        }
    }

    async okClicked(){
        console.log("ok clicked");
        for (const key in this.newQuery) {
            this.newQuery[key] = typeof this.newQuery[key] === "string"  && this.newQuery[key].length == 0 ? null :  this.newQuery[key];
        }

        console.log("post/put query:");
        console.log(this.newQuery);
        
        let response: Response
        if (this.newQuery.query_id === null){ //add new
            response = await fetch(window.SERVER_URL + "/users/" + this.$store.state.User.identity.user_id + "/re_queries", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + this.$store.state.User.access_token
                },
                body: JSON.stringify(this.newQuery)
            })
        } else {
            response = await fetch(window.SERVER_URL + "/users/" + this.$store.state.User.identity.user_id + "/re_queries/" + this.newQuery.query_id, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + this.$store.state.User.access_token
                },
                body: JSON.stringify(this.newQuery)
            })
        }

        if (!response.ok){
            this.showErr = true
            this.errMsg = "Įvyko klaida ištrinant paiešką."
            return
        }
        this.getQueries();
        this.newQuery = this.defaultQueryValues()
    }

    async getQueries(){
        const response = await fetch(window.SERVER_URL + "/users/" + this.$store.state.User.identity.user_id + "/re_queries", {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + this.$store.state.User.access_token
            }
        })

        if(!response.ok){
            this.showErr = true
            this.errMsg = "Įvyko klaida kraunant paieškas."
            return
        }

        const data: ReQueryResponse[] = await response.json()
        console.log(data);
        this.queries = data.reverse();
    }
}
    

</script>

<style lang="scss">

.domo-text {
    color: #7eba47;
}

.skelbiu-text {
    color: #ffcc01;
}

.domo-bg {
    background-color: #7eba47;
}

.skelbiu-bg {
    background-color: #ffcc01;
}

</style>