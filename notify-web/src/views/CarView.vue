<template>
<div>
   <b-row class="mt-5 mb-3">
        <b-col>
            <h2>
                {{header}}
            </h2>
        </b-col>
   </b-row>
   <b-row>
       <b-col cols="12" sm="12" md="8">
           <lingallery v-if="car.picture_href && car.picture_href.length > 0" width="100%" :iid.sync="picId" :items="car.picture_href"></lingallery>
            <b-img v-if="!car.picture_href || car.picture_href.length == 0" fluid-grow="" src="/img/icons/no-image-icon.png"></b-img> 
       </b-col>
       <b-col cols="12" sm="12" md="4">
           <b-row v-if="car.price" class="mt-2">
               <b-col cols="5">
                   Kaina
               </b-col>
               <b-col>
                   <h3 class="param">{{car.price}} €</h3>
               </b-col>
           </b-row>

           <b-row v-if="car.export_price" class="mt-2">
               <b-col cols="5">
                   Kaina eksportui
               </b-col>
               <b-col>
                   <h3 class="param">{{car.export_price}} €</h3>
               </b-col>
           </b-row>

           <b-row v-if="car.make_name" class="mt-2">
               <b-col cols="5">
                   Markė
               </b-col>
               <b-col class="param">
                   {{car.make_name}}
               </b-col>
           </b-row>

            <b-row v-if="car.model_name" class="mt-2">
               <b-col cols="5">
                   Modelis
               </b-col>
               <b-col class="param">
                   {{car.model_name}}
               </b-col>
           </b-row>

           <b-row v-if="car.year" class="mt-2">
               <b-col cols="5">
                   Metai
               </b-col>
               <b-col class="param">
                   {{car.year}} m.
               </b-col>
           </b-row>

           <b-row v-if="car.engine" class="mt-2">
               <b-col cols="5">
                   Variklis
               </b-col>
               <b-col class="param">
                   {{car.engine}}
               </b-col>
           </b-row>

            <b-row v-if="car.fuel_name" class="mt-2">
               <b-col cols="5">
                   Kuro tipas
               </b-col>
               <b-col class="param">
                   {{car.fuel_name}}
               </b-col>
           </b-row>

           <b-row v-if="car.body_type_name" class="mt-2">
               <b-col cols="5">
                   Kėbulo tipas
               </b-col>
               <b-col class="param">
                   {{car.body_type_name}}
               </b-col>
           </b-row>

           <b-row v-if="car.color" class="mt-2">
               <b-col cols="5">
                   Spalva
               </b-col>
               <b-col class="param">
                   {{car.color}}
               </b-col>
           </b-row>

           <b-row v-if="car.gearbox" class="mt-2">
               <b-col cols="5">
                   Pavarų dėžė
               </b-col>
               <b-col class="param">
                   {{car.gearbox}}
               </b-col>
           </b-row>

           <b-row v-if="car.driven_wheels" class="mt-2">
               <b-col cols="5">
                   Varomieji ratai
               </b-col>
               <b-col class="param">
                   {{car.driven_wheels}}
               </b-col>
           </b-row>

           <b-row v-if="car.damage" class="mt-2">
               <b-col cols="5">
                   Defektai
               </b-col>
               <b-col class="param">
                   {{car.damage}}
               </b-col>
           </b-row>

           <b-row v-if="car.steering_column" class="mt-2">
               <b-col cols="5">
                   Vairo padėtis
               </b-col>
               <b-col class="param">
                   {{car.steering_column}}
               </b-col>
           </b-row>

           <b-row v-if="car.door_count" class="mt-2">
               <b-col cols="5">
                   Durų skaičius
               </b-col>
               <b-col class="param">
                   {{car.door_count}}
               </b-col>
           </b-row>

           <b-row v-if="car.cylinder_count" class="mt-2">
               <b-col cols="5">
                   Cilindrų skaičius
               </b-col>
               <b-col class="param">
                   {{car.cylinder_count}}
               </b-col>
           </b-row>

           <b-row v-if="car.gear_count" class="mt-2">
               <b-col cols="5">
                   Pavarų skaičius
               </b-col>
               <b-col class="param">
                   {{car.gear_count}}
               </b-col>
           </b-row>

           <b-row v-if="car.seat_count" class="mt-2">
               <b-col cols="5">
                   Sėdimų vietų skaičius
               </b-col>
               <b-col class="param">
                   {{car.seat_count}}
               </b-col>
           </b-row>

           <b-row v-if="car.ts_to" class="mt-2">
               <b-col cols="5">
                   TA iki
               </b-col>
               <b-col class="param">
                   {{car.ts_to ? new Date(car.ts_to).toISOString().split('T')[0] : null}}
               </b-col>
           </b-row>

           <b-row v-if="car.vin_code" class="mt-2">
               <b-col cols="5">
                   VIN kodas
               </b-col>
               <b-col class="param">
                   {{car.vin_code}}
               </b-col>
           </b-row>

           <b-row v-if="car.wheels" class="mt-2">
               <b-col cols="5">
                   Ratlankiai
               </b-col>
               <b-col class="param">
                   {{car.wheels}}
               </b-col>
           </b-row>

           <b-row v-if="car.first_reg_country" class="mt-2">
               <b-col cols="5">
                   Pirmosios registracijos šalis
               </b-col>
               <b-col class="param">
                   {{car.first_reg_country}}
               </b-col>
           </b-row>

           <b-row v-if="car.el_range" class="mt-2">
               <b-col cols="5">
                   Rida su vienu įkrovimu
               </b-col>
               <b-col class="param">
                   {{car.el_range}} km
               </b-col>
           </b-row>

           <b-row v-if="featuresComp" class="mt-5">
               <b-col class="param" cols="3" sm="5" md="5" lg="4">
                   <div>Ypatybės</div>
               </b-col>
               <b-col class="border-bottom mb-2"></b-col>
           </b-row>

           <b-row v-if="featuresComp" class="mt-2">
               <b-col>
                   <ul>
                       <li v-for="(category, i) in featuresComp.categories" :key="category">
                           {{category}}
                           <ul>
                               <li v-for="feature in featuresComp.features[i]" :key="feature">{{feature}}</li>
                           </ul>
                        </li>
                   </ul>
               </b-col>
           </b-row>

           <b-row v-if="car.comments" class="mt-5">
               <b-col class="param" cols="4" sm="6" md="6" lg="4">
                   <div>Komentarai</div>
               </b-col>
               <b-col class="border-bottom mb-2"></b-col>
           </b-row>

           <b-row v-if="car.comments" class="mt-2">
               <b-col>
                   <div v-for="c in car.comments" :key="c">{{c}}</div>
               </b-col>
           </b-row>

           <b-row v-if="car.phone || car.location" class="mt-5">
               <b-col class="param" cols="3" sm="5" md="5" lg="4">
                   <div>Kontaktai</div>
               </b-col>
               <b-col class="border-bottom mb-2"></b-col>
           </b-row>

            <b-row v-if="car.phone" class="mt-2">
                <b-col cols="3">
               </b-col>
               <b-col cols="7" class="param">
                   Tel. nr.: {{car.phone}}
               </b-col>
           </b-row>

           <b-row v-if="car.location" class="mt-2">
               <b-col cols="3">
               </b-col>
               <b-col class="param">
                   {{car.location}}
               </b-col>
           </b-row>
           <b-row v-if="car.location" class="mt-2">
               <b-col cols="3">
               </b-col>
               <b-col class="font-italic">
                   <a rel="noopener noreferrer" target="_blank" :href="car.href">{{hrefTitle}}</a>
               </b-col>
           </b-row>
       </b-col>
       
   </b-row>
</div>
</template>
<script>
export default {
    name: 'CarView',
	components: {
	},
  data () {
    return {
        car: {autob_id: null
                ,autobilis_fuel_id: 0
                ,autobilis_id: 0
                ,autobilis_make_id: 143
                ,autobilis_model_id: 960
                ,autog_id: null
                ,autop_id: 9206815
                ,autoplius_fuel_id: 30
                ,autoplius_id: 4
                ,autoplius_make_id: 99
                ,autoplius_model_id: 1343
                ,'body_styles.id': 1
                ,body_type: 1
                ,body_type_name: "Sedanas"
                ,color: null
                ,comments: "Puikiai važiuojantis automobilis, pakeista daug detalių naujomis."
                ,cylinder_count: null
                ,damage: null
                ,deleted: 0
                ,door_count: null
                ,driven_wheels: "Priekiniai varantys ratai"
                ,engine: "2200 cm³, 135 AG (100kW)"
                ,export_price: null
                ,features: ""
                ,fuel_name: "Benzinas"
                ,fuel_overall: null
                ,fuel_overland: null
                ,fuel_type: 2
                ,'fuel_types.fuel_name': "Benzinas"
                ,'fuel_types.id': 2
                ,fuel_urban: null
                ,gear_count: null
                ,gearbox: "Mechaninė"
                ,href: "https://autoplius.lt/skelbimai/audi-90-2-2-l-sedanas-1984-benzinas-9206815.html"
                ,id: 794
                ,location: "Panevėžys, Lietuva"
                ,make: 10
                ,make_id: 10
                ,make_name: "Audi"
                ,'makes.id': 10
                ,'makes.make': "Audi"
                ,mileage: 230844
                ,model: 11019
                ,model_name: "90"
                ,'models.id': 11019
                ,'models.model_name': "90"
                ,name: "Sedanas"
                ,phone: "+370 684 72168"
                ,picture_href: "https://autoplius-img.dgn.lt/ann_3_88848153/audi-90-2-2-l-sedanas-1984-benzinas.jpg"
                ,price: 2999
                ,seat_count: 5
                ,steering_column: "Kairėje"
                ,ts_to: null
                ,vin_code: null
                ,weight: 1100
                ,wheels: null
                ,when_scraped: 1588442155
                ,year: "1984"},
        tmp: {},
        picId: null
    }
  },

	methods: {
		async getCar() {
            console.log("getcar");
            this.tmp = {
                autob_id: null
                ,autobilis_fuel_id: 0
                ,autobilis_id: 0
                ,autobilis_make_id: 143
                ,autobilis_model_id: 960
                ,autog_id: null
                ,autop_id: 9206815
                ,autoplius_fuel_id: 30
                ,autoplius_id: 4
                ,autoplius_make_id: 99
                ,autoplius_model_id: 1343
                ,'body_styles.id': 1
                ,body_type: 1
                ,body_type_name: "Sedanas"
                ,color: null
                ,comments: "Puikiai važiuojantis automobilis, pakeista daug detalių naujomis."
                ,cylinder_count: null
                ,damage: null
                ,deleted: 0
                ,door_count: null
                ,driven_wheels: "Priekiniai varantys ratai"
                ,engine: "2200 cm³, 135 AG (100kW)"
                ,export_price: null
                ,features: ""
                ,fuel_name: "Benzinas"
                ,fuel_overall: null
                ,fuel_overland: null
                ,fuel_type: 2
                ,'fuel_types.fuel_name': "Benzinas"
                ,'fuel_types.id': 2
                ,fuel_urban: null
                ,gear_count: null
                ,gearbox: "Mechaninė"
                ,href: "https://autoplius.lt/skelbimai/audi-90-2-2-l-sedanas-1984-benzinas-9206815.html"
                ,id: 794
                ,location: "Panevėžys, Lietuva"
                ,make: 10
                ,make_id: 10
                ,make_name: "Audi"
                ,'makes.id': 10
                ,'makes.make': "Audi"
                ,mileage: 230844
                ,model: 11019
                ,model_name: "90"
                ,'models.id': 11019
                ,'models.model_name': "90"
                ,name: "Sedanas"
                ,phone: "+370 684 72168"
                ,picture_href: "https://autoplius-img.dgn.lt/ann_3_88848153/audi-90-2-2-l-sedanas-1984-benzinas.jpg"
                ,price: 2999
                ,seat_count: 5
                ,steering_column: "Kairėje"
                ,ts_to: null
                ,vin_code: null
                ,weight: 1100
                ,wheels: null
                ,when_scraped: 1588442155
                ,year: "1984"
            }
            
            const response = await fetch(window.SERVER_URL + "/queries/" + this.$route.params.query_id + "/cars/" + this.$route.params.car_id, {
                headers: {
                    'Authorization': 'Bearer ' + this.$store.state.User.access_token
                }
            });
            const data = await response.json();
            data.comments = data.comments.replace(/<div class="announcement-description">/, "").replace(/<\/div>/g, "")
                .replace(/<span>/, "").replace(/<\/span>/, "").replace(/<div class="comments" itemprop="description">/, "").split('<br>')
            this.car = data
            
            for (let i = 0; i < this.car.picture_href.length; i++) {
                this.car.picture_href[i] = {
                    src: this.car.picture_href[i],
                    thumbnail: this.car.picture_href[i],
                    id: i
                }
            }


        },

        autopFeatures() {
            const lines = this.car.features.split('\n')
            const categories = []
            const features = []
            let counter = 0
            for (const line of lines) {
                if (!line)
                    continue
                const tmp = line.split(':')
                categories.push(tmp[0])
                features.push([])
                const fts = tmp[1].split(',')
                for (const ft of fts) 
                    features[counter].push(ft)
                
                counter++;
            }
            return {categories: categories, features: features}
        },

        autogFeatures() {
            const lines = this.car.features.split(',')
            
            return {categories: lines, features: []}
        }
    },
    
    computed: {
        header() {
            const hdr = `${this.car.make_name} ${this.car.model_name} ${this.car.fuel_name} ${this.car.year} m` 
            return hdr
        },

        featuresComp () {
            if (!this.car.features)
                return null;
            if (this.car.autop_id)
                return this.autopFeatures()
            if (this.car.autog_id || this.car.autob_id)
                return this.autogFeatures()
            
            return null
        },

        hrefTitle() {
            if (this.car.autob_id) 
                return "Autobilis.lt nuoroda"
            else if (this.car.autog_id) 
                return "Autogidas.lt nuoroda"
            else 
                return "Autoplius.lt nuoroda" 
        }   
    },

    created() {
        window.scrollTo(0,0)
        this.getCar();
        
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
