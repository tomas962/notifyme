<template>
<div v-if="re_ad">
   <b-row class="mt-5 mb-3">
        <b-col>
            <h2>
                {{re_ad.title}}
            </h2>
        </b-col>
   </b-row>
   <b-row>
       <b-col cols="12" sm="12" md="8">
           <lingallery v-if="re_ad.picture_href && re_ad.picture_href.length > 0" width="100%" :iid.sync="picId" :items="re_ad.picture_href"></lingallery>
            <b-img v-if="!re_ad.picture_href || re_ad.picture_href.length == 0" fluid-grow="" src="/img/icons/no-image-icon.png"></b-img> 
       </b-col>
       <b-col cols="12" sm="12" md="4">
           <b-row v-if="re_ad.price" class="mt-2">
               <b-col cols="5">
                   Kaina
               </b-col>
               <b-col>
                   <h3 class="param">{{re_ad.price}} €</h3>
               </b-col>
           </b-row>
           <b-row v-if="re_ad.price_per_area" class="mt-2">
               <b-col cols="5">
                   Ploto vieneto kaina
               </b-col>
               <b-col class="param">
                   {{re_ad.price_per_area}}
               </b-col>
           </b-row>
           <b-row v-if="re_ad.city" class="mt-2">
               <b-col cols="5">
                   Miestas
               </b-col>
               <b-col class="param">
                   {{re_ad.city}}
               </b-col>
           </b-row>
           <b-row v-if="re_ad.village" class="mt-2">
               <b-col cols="5">
                   Gyvenvietė
               </b-col>
               <b-col class="param">
                   {{re_ad.village}}
               </b-col>
           </b-row>
           <b-row v-if="re_ad.neighborhood" class="mt-2">
               <b-col cols="5">
                   Mikrorajonas
               </b-col>
               <b-col class="param">
                   {{re_ad.neighborhood}}
               </b-col>
           </b-row>
            <b-row v-if="re_ad.street" class="mt-2">
               <b-col cols="5">
                   Gatvė
               </b-col>
               <b-col class="param">
                   {{re_ad.street}}
               </b-col>
           </b-row>
           <b-row v-if="re_ad.house_type" class="mt-2">
               <b-col cols="5">
                   Tipas
               </b-col>
               <b-col class="param">
                   {{re_ad.house_type}}
               </b-col>
           </b-row>
           <b-row v-if="re_ad.type" class="mt-2">
               <b-col cols="5">
                   Pastato tipas
               </b-col>
               <b-col class="param">
                   {{re_ad.type}}
               </b-col>
           </b-row>
           <b-row v-if="re_ad.area" class="mt-2">
               <b-col cols="5">
                   Plotas
               </b-col>
               <b-col class="param">
                   {{re_ad.area}}
               </b-col>
           </b-row>
           <b-row v-if="re_ad.heating" class="mt-2">
               <b-col cols="5">
                   Šildymas
               </b-col>
               <b-col class="param">
                   {{re_ad.heating}}
               </b-col>
           </b-row>
           <b-row v-if="re_ad.room_count" class="mt-2">
               <b-col cols="5">
                   Kamb. sk.
               </b-col>
               <b-col class="param">
                   {{re_ad.room_count}}
               </b-col>
           </b-row>
           <b-row v-if="re_ad.site_area" class="mt-2">
               <b-col cols="5">
                   Sklypo plotas
               </b-col>
               <b-col class="param">
                   {{re_ad.site_area}}
               </b-col>
           </b-row>
           <b-row v-if="re_ad.installation" class="mt-2">
               <b-col cols="5">
                   Įrengimas
               </b-col>
               <b-col class="param">
                   {{re_ad.installation}}
               </b-col>
           </b-row>
           <b-row v-if="re_ad.energy_class" class="mt-2">
               <b-col cols="5">
                   Energijos klasė
               </b-col>
               <b-col class="param">
                   {{re_ad.energy_class}}
               </b-col>
           </b-row>
           <b-row v-if="re_ad.floor" class="mt-2">
               <b-col cols="5">
                   Aukštas
               </b-col>
               <b-col class="param">
                   {{re_ad.floor}}
               </b-col>
           </b-row>
           <b-row v-if="re_ad.floor_count" class="mt-2">
               <b-col cols="5">
                   Aukštų skaičius
               </b-col>
               <b-col class="param">
                   {{re_ad.floor_count}}
               </b-col>
           </b-row>
           <b-row v-if="re_ad.gas" class="mt-2">
               <b-col cols="5">
                   Dujos
               </b-col>
               <b-col class="param">
                   {{re_ad.gas}}
               </b-col>
           </b-row>
           <b-row v-if="re_ad.sewage" class="mt-2">
               <b-col cols="5">
                   Kanalizacija
               </b-col>
               <b-col class="param">
                   {{re_ad.sewage}}
               </b-col>
           </b-row>
           <b-row v-if="re_ad.water" class="mt-2">
               <b-col cols="5">
                   Vandentiekis
               </b-col>
               <b-col class="param">
                   {{re_ad.water}}
               </b-col>
           </b-row>
           <b-row v-if="re_ad.year" class="mt-2">
               <b-col cols="5">
                   Metai
               </b-col>
               <b-col class="param">
                   {{re_ad.year}}
               </b-col>
           </b-row>
           <b-row v-if="re_ad.year_reconstructed" class="mt-2">
               <b-col cols="5">
                   Renovacijos metai
               </b-col>
               <b-col class="param">
                   {{re_ad.year_reconstructed}}
               </b-col>
           </b-row>

            <b-row v-if="features.length > 0" class="mt-5">
               <b-col class="param" cols="3" sm="5" md="5" lg="4">
                   <div>Ypatybės</div>
               </b-col>
               <b-col class="border-bottom mb-2"></b-col>
           </b-row>

           <b-row v-if="features.length > 0" class="mt-2">
               <b-col>
                   <ul>
                       <li v-for="feature in features" :key="feature">
                           {{feature[0].toUpperCase() + feature.slice(1)}}
                       </li>
                   </ul>
               </b-col>
           </b-row>

           <b-row v-if="re_ad.description" class="mt-5">
               <b-col class="param" cols="4" sm="6" md="6" lg="4">
                   <div>Komentarai</div>
               </b-col>
               <b-col class="border-bottom mb-2"></b-col>
           </b-row>
           <b-row v-if="re_ad.description" class="mt-2">
               <b-col>
                   <div v-for="c in comments" :key="c">
                       {{c}}<br>
                   </div>
               </b-col>
           </b-row>

           <b-row v-if="re_ad.phone || re_ad.href" class="mt-5">
               <b-col class="param" cols="3" sm="5" md="5" lg="4">
                   <div>Kontaktai</div>
               </b-col>
               <b-col class="border-bottom mb-2"></b-col>
           </b-row>

           <b-row v-if="re_ad.phone" class="mt-2">
                <b-col cols="3">
               </b-col>
               <b-col cols="7" class="param">
                   Tel. nr.: {{re_ad.phone}}
               </b-col>
           </b-row>

           <b-row v-if="hrefTitle" class="mt-2">
               <b-col cols="3">
               </b-col>
               <b-col class="font-italic">
                   <a rel="noopener noreferrer" target="_blank" :href="re_ad.href">{{hrefTitle}}</a>
               </b-col>
           </b-row>
       </b-col> 
       
   </b-row>
</div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import {ReAd} from '@/models/interfaces'

@Component
export default class CarComp extends Vue {
    re_ad: ReAd = {
        area: "",
        city: "",
        city_id: 0,
        description: "",
        domo_id: null,
        energy_class: "",
        features: "",
        floor: "",
        floor_count: null,
        gas: "",
        heating: "",
        house_type: "",
        href: "",
        id: null,
        installation: "",
        neighborhood: "",
        phone: "",
        price: null,
        price_per_area: "",
        room_count: null,
        sewage: "",
        site_area: "",
        skelbiu_id: null,
        street: "",
        title: "",
        type: "",
        village: "",
        water: "",
        when_scraped: null,
        year: "",
        year_reconstructed: "",
        pictures: [],
        picture_href: []
    }
    picId = null;
    
    created(){
        this.getReAd();
    }

    async getReAd(){
        const response = await fetch(window.SERVER_URL + "/users/" + this.$store.state.User.identity.user_id +"/re_queries/" + this.$route.params.query_id + "/re_ads/" + this.$route.params.re_ad_id, {
            headers: {
                'Authorization': 'Bearer ' + this.$store.state.User.access_token
            }
        });
        const data = await response.json();
        
        console.log(data);
        
        this.re_ad = data
        if(this.re_ad){
            this.re_ad.picture_href = []
            for (let i = 0; i < this.re_ad.pictures.length; i++) {
                this.re_ad.picture_href.push({
                    src: this.re_ad.pictures[i],
                    thumbnail: this.re_ad.pictures[i],
                    id: i
                })
            }
        }

    }

    get features(){
        if (this.re_ad.features)
            return this.re_ad.features.split("|")
        else 
            return []
    }

    get comments(){
        if (this.re_ad.description) {
            return this.re_ad.description.split("\n")
        } else {
            return []
        }
    }
    
    get hrefTitle() {
        if (this.re_ad.domo_id)
            return "Domoplius.lt nuoroda"
        if (this.re_ad.skelbiu_id)
            return "Skelbiu.lt nuoroda"
        else
            return "Nuoroda"
    }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

.car-pic {
    max-height: 800px;
    max-width: 730px;
}

.param {
    font-weight: bold;
}

</style>
