<template>
  <div>
    <a href="#" v-on:click="sortCars((a, b) => a.price - b.price)">SORT </a>
    <CarComp v-for="car in cars" :key="car.id" :car="car" />

  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import CarComp from '@/components/Car.vue'
import {
  State,
  Getter,
  Action,
  Mutation,
  namespace
} from 'vuex-class'
import {Car} from '../store/modules/cars'

const carsns = namespace('CarList')

@Component({
  components: {
    CarComp
  }
})
export default class CarList extends Vue {

  @carsns.State
  public cars?: Car[];

  @carsns.Action
  public fetchCars!: () => void

  @carsns.Action
  public sortCars: (sortFn: (a: Car, b: Car) => number) => void

  created() {
    console.log("CREATED");
    this.fetchCars()
  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>
