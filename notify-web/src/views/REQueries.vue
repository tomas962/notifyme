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
                            </b-col>
                            <b-col cols="6">
                                <b-form-group label="Plotas">
                                    <b-row>
                                        <b-col cols="6">
                                            <b-form-input number v-model.number="newQuery.area_from" type="number" placeholder="Nuo"></b-form-input>
                                        </b-col>
                                        <b-col cols="6">
                                            <b-form-input number v-model.number="newQuery.area_to" type="number" placeholder="Iki"></b-form-input>
                                        </b-col>
                                    </b-row>
                                </b-form-group>
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
                                            <b-form-select v-model="newQuery.type_id" :options="queryFormData.reTypes"></b-form-select>
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
                        <!-- <b-row>
                            <b-col>
                                <b-form-select v-model="newQuery.body_style_id" :options="queryFormData.bodyStyles" ></b-form-select>
                            </b-col>
                            <b-col>
                                <b-form-select v-model="newQuery.fuel_id" :options="queryFormData.fuelTypes" ></b-form-select>
                            </b-col>
                        </b-row>
                        <b-row >getFormData
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
                        </b-row> -->
                        
                    </b-form>
                </b-modal>
            </b-col>

        </b-row>
    </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import {SelectOption} from "@/models/interfaces"

interface ReQueryDtata {
    cities: SelectOption[];
    categories: SelectOption[];
    reTypes: SelectOption[];
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

interface ReQuery {
    city_id: number|null;
    category_id: number|null;
    price_from: number|null;
    price_to: number|null;
    year_from: number|null;
    year_to: number|null;
    area_from: number|null;
    area_to: number|null;
    type_id: number|null;

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
        type_id: null
    }
    queryFormData: ReQueryDtata = {
        cities: [],
        categories: [],
        reTypes: []
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

    getFormData(){
        console.log();
        this.getCities();
        this.getCategories();
        this.getReTypes();
    }
    onCancelClick(){
        console.log();
        
    }
    okClicked(){

        console.log();
    }
}
    

</script>

<style lang="scss" scoped>

</style>