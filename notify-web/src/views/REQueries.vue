<template>
    <div>
        

        <b-row class="mt-3">
            <b-col cols="8"><h2>Jūsų Paieškos - Nekilnojamasis turtas</h2></b-col>
            <b-col>
                <b-button v-on:click="getFormData();" class="btn-info" v-b-modal.queryEditModal>Nauja paieška</b-button>
                <b-modal v-on:cancel="onCancelClick()" v-on:ok="okClicked()" ok-title="Išsaugoti" cancel-title="Atšaukti" id="queryEditModal" :title='editForm ? "Redaguojama paieška" : "Nauja paieška"' size="lg">
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
                                <div>
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
                                        <b-col cols="6">
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
                                            <b-form-select v-model="newQuery.house_type_id" :options="queryFormData.reHouseTypes"></b-form-select>
                                        </b-col>
                                        <b-col>
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
    </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import {SelectOption} from "@/models/interfaces"

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

@Component
export default class REQueries extends Vue {

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
    created(){
        console.log("requeries created");
        
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
    onCancelClick(){
        console.log();
        
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
            query_id: null
        }
    }

    async okClicked(){
        console.log("ok clicked");
        for (const key in this.newQuery) {
            this.newQuery[key] = typeof this.newQuery[key] === "string"  && this.newQuery[key].length == 0 ? null :  this.newQuery[key];
        }

        console.log("post/put query:");
        console.log(this.newQuery);
        
        
        if (this.newQuery.query_id === null){ //add new
            const response = await fetch(window.SERVER_URL + "/users/" + this.$store.state.User.identity.user_id + "/re_queries", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + this.$store.state.User.access_token
                },
                body: JSON.stringify(this.newQuery)
            })
        }

        // this.getQueries();
        this.newQuery = this.defaultQueryValues()
    }
}
    

</script>

<style lang="scss" scoped>

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