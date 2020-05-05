<template>
<div>
    <a href="#" v-on:click="sortCars((a, b) => a.price - b.price);">SORT </a>
    <b-row class="text-center">
        <b-col>
            <b-pagination 
            v-model="currentPage"
            :total-rows="cars.length"
            :per-page="perPage"
            align="center"
            ></b-pagination>
        </b-col>
    </b-row>
    
    <CarComp v-for="car in carPage" :key="car.id" :car="car" />
</div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import CarComp from '@/components/Car.vue'
import {namespace} from 'vuex-class'
import {Car} from '../store/modules/cars'

const carsns = namespace('CarList')
const UI = namespace('UIState')

@Component({
components: {
    CarComp
}
})
export default class CarList extends Vue {
    query_id = -1;

    perPage = 10;

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


    @carsns.State
    public cars!: Car[];

    @carsns.Action
    public fetchCars!: (query_id: {query_id: number}) => void

    @carsns.Action
    public sortCars!: (sortFn: (a: Car, b: Car) => number) => void

    created() {
        if (this.currentPage == null) {
            this.currentPage = 1
        }
        this.query_id = parseInt(this.$route.params.query_id, 10);
        this.fetchCars({query_id: this.query_id});
        console.log("_currentPage:");
        console.log(this.currentPage);
        
    }

    get carPage() {
        const start = (this.currentPage-1) * this.perPage
        const end = start + this.perPage
        console.log(start);
        console.log(end);
        
        return this.cars.slice(start, end);
    }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>
