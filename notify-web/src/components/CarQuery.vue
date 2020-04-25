<template>
    <b-row class=" rounded border mt-3">
        <b-col>
            Markė: <strong>{{query.make_model ? query.make_model.make : ""}}</strong>
        </b-col>
        <b-col>
            Modelis: <strong>{{query.make_model ? query.make_model.model_name : ""}}</strong>
        </b-col>
        <b-col>
            Kaina: nuo {{query.car_query.price_from}} € iki {{query.car_query.price_to}} €
        </b-col>
        <b-col>
            Metai: nuo {{query.car_query.year_from}} iki {{query.car_query.year_to}}
        </b-col>
    </b-row>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import {CarQueryResponse} from "@/models/interfaces"

@Component
export default class CarQueryComp extends Vue {
    @Prop() query!: CarQueryResponse
}
</script>

<style lang="scss" scoped>

</style>