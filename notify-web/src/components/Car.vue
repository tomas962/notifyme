<template>
    <b-row class=" rounded border-right border-top border-bottom mt-4">
        <b-col class="pl-0 pr-0 rounded-left" cols="12" sm="7" lg="4">
            <img width="100%" height="100%" src="https://img.autogidas.lt/4_15_169276666/volkswagen-passat-cc-tsi-coupe-2010.jpg">
        </b-col>
        <b-col>
            <b-row :class="'autop'">
                <b-col class="mt-3 " lg="4">
                    <h5>{{car.make}}</h5>
                </b-col>
            </b-row>
            <b-row>
                <b-col class="mt-3 autog-price" lg="4">
                    <h4 class="border border-success rounded"  >500 $</h4>
                </b-col>
            </b-row>
            <b-row>
                <b-col class="mt-lg-3" cols="12" md="8">
                    <p>1.7 l., Dyzelinas, 2011 m, Mechaninė, 81 kW</p>
                </b-col>
            </b-row>
             <b-row>
                <b-col class="" cols="12" md="8">
                    <p>165 000 km., Universalas, Kaunas</p>
                </b-col>
            </b-row>
        </b-col>
    </b-row>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import {Car} from '@/store/modules/cars'

@Component
export default class CarComp extends Vue {
    @Prop() car!: Car

    created() {
        console.log("CALLED");
        console.log(this.car);
    }
}
</script>

<style lang="scss" scoped>
.img-col {
    margin-left: -100px;
}

.autog {
    background-color: #FEA638;
}

.autop {
    background-color: #1174b9;
}

.autob {
    background-color: #df1d38;
}

.autog-price {
    color: #FEA638;
}

.autop-price {
    color: #1174b9;
}

.autob-price {
    color: #df1d38;
}
</style>