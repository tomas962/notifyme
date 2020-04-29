<template>
    <b-row  class=" rounded border-right border-top border-bottom mt-4">
        <b-col class="pl-0 pr-0 rounded-left" cols="12" sm="7" lg="4">
            <img width="100%" height="100%" :src="car.picture_href">
        </b-col>
        <b-col>
            <b-row :class="headerColorClass">
                <b-col class="mt-3 " lg="4">
                    <h4>{{car.make_name}}, {{car.model_name}}</h4>
                </b-col>
            </b-row>
            <b-row>
                <b-col class="mt-3" lg="4" offset="2" cols="8" offset-lg="0">
                    <h4 :class="priceClass + ' border border-success rounded text-center'" >{{car.price}} €</h4>
                </b-col>
            </b-row>
            <b-row>
                <b-col class="mt-lg-3" cols="12" md="8">
                    <p>{{car.engine}}, {{car.fuel_name}}, {{car.year}} m. , {{car.gearbox}}</p>
                </b-col>
            </b-row>
             <b-row>
                <b-col class="" cols="12" md="8">
                    <p>{{car.mileage ? car.mileage + " km.," : ""}} {{car.body_type_name}}, {{car.location ? car.location.split(',')[1] : ""}}</p>
                </b-col>
                <b-col>
                    <a :href="car.href">Nuoroda</a>
                </b-col>
            </b-row>
        </b-col>
    </b-row>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import {Car} from '../store/modules/cars'

@Component
export default class CarComp extends Vue {
    @Prop() car!: Car

    get headerColorClass(): string {
        if (this.car.autob_id)
            return "autob"
        if (this.car.autog_id)
            return "autog"
        if (this.car.autop_id)
            return "autop"
        return ""
    }
    
    get priceClass(): string {
        if (this.car.autob_id)
            return "autob-price"
        if (this.car.autog_id)
            return "autog-price"
        if (this.car.autop_id)
            return "autop-price"
        return ""
    }
    
    created() {
        this.car.price *= 10;
    }
}
</script>

<style lang="scss">
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