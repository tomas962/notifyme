<template>
<router-link style="text-decoration: none; color: inherit;" :to="'./re_ads/' + re_ad.id" tag="a">
    <b-row  class="pointer hoverable rounded border-right border-top border-bottom mt-5 mt-sm-4">
        <b-col class="pl-0 pr-0 rounded-left" cols="12" sm="7" lg="4">
            <b-img :src="re_ad.pictures && re_ad.pictures.length > 0 ? re_ad.pictures[0] : '/img/icons/no-image-icon.png' " fluid-grow></b-img>
            <!-- <img width="100%" height="100%" :src="car.picture_href"> -->
        </b-col>
        <b-col>
            <b-row :class="headerColorClass">
                <b-col class="mt-3 ">
                    <h4>{{re_ad.title}}</h4>
                </b-col>
            </b-row>
            <b-row>
                <b-col class="mt-3" lg="4" offset="2" cols="8" offset-lg="0">
                    <h4 :class="priceClass + ' border border-success rounded text-center'" >{{re_ad.price}} €</h4>
                </b-col>
            </b-row>
            <b-row>
                <b-col class="mt-lg-3" cols="12" md="8">
                    <p>{{description}}</p>
                </b-col>
            </b-row>
             <!-- <b-row>
                <b-col class="" cols="12" md="8">
                    <p>{{car.mileage ? car.mileage + " km.," : ""}} {{car.body_type_name}}, {{car.location}}</p>
                </b-col>
                <b-col>
                    <a :href="car.href">Nuoroda</a>
                </b-col>
            </b-row> -->
        </b-col>
    </b-row>
</router-link>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import {ReAd} from '@/models/interfaces'

@Component
export default class CarComp extends Vue {
    @Prop() re_ad!: ReAd

    get headerColorClass(): string {
        if (this.re_ad.skelbiu_id)
            return "skelbiu-bg"
        if (this.re_ad.domo_id)
            return "domo-bg"
        return ""
    }
    
    get priceClass(): string {
        if (this.re_ad.domo_id)
            return "domo-text"
        if (this.re_ad.skelbiu_id)
            return "skelbiu-text"
        return ""
    }
    
    get description(): string {
        const re_ad = this.re_ad
        return `${re_ad.area ? re_ad.area + ' | ' : ''}${re_ad.room_count ? re_ad.room_count + ' kamb. | ' : ''}
            ${re_ad.floor_count ? re_ad.floor_count + ' aukštai | ' : ''}${re_ad.year ? re_ad.year + ' m | ' : ''}
            ${re_ad.floor ? re_ad.floor + ' | ' : ''}${re_ad.city ? re_ad.city + ' | ' : ""}${re_ad.site_area ? "Sklypo plotas: " + re_ad.site_area : ""}`
    }
}
</script>

<style lang="scss">
.img-col {
    margin-left: -100px;
}

</style>