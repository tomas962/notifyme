<template>
    <b-row class="ml-2">
        <CarQueryComp  v-for="query1 in queries4" :key="query1.car_query.id" :query="query1"></CarQueryComp>
    </b-row>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import CarQueryComp from './CarQuery.vue'
import {CarQueryResponse} from "@/models/interfaces"

@Component({
    components: {
        CarQueryComp
    }
})
export default class CarQueryRowComp extends Vue {
    @Prop() queries4!: CarQueryResponse[]

}
</script>

<style lang="scss" scoped>

</style>