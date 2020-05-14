<template>
    <b-row class="ml-2">
        <ReQueryComp  v-for="query1 in queries4" :key="query1.id" :query="query1"></ReQueryComp>
    </b-row>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import ReQueryComp from './ReQuery.vue'
import {ReQueryResponse} from "@/models/interfaces"

@Component({
    components: {
        ReQueryComp
    }
})
export default class ReQueryRowComp extends Vue {
    @Prop() queries4!: ReQueryResponse[]

}
</script>

<style lang="scss" scoped>

</style>