import { VuexModule, Module, Mutation, Action, } from 'vuex-module-decorators'

class Car {
    autob_id?: number
    autog_id?: number
    autop_id?: number
    body_type?: number
    color?: string
    comments?: string
    cylinder_count?: number
    damage?: string
    door_count?: string
    driven_wheels?: string
    engine?: string
    export_price?: number
    features?: string
    fuel_overall?: number
    fuel_overland?: number
    fuel_type?: number
    fuel_urban?: number
    gear_count?: number
    gearbox?: string
    href?: string
    id?: number
    make?: number
    model?: number
    picture_href?: string
    price?: number
    query_id?: number
    seat_count?: number
    steering_column?: string
    ts_to?: string
    vin_code?: string
    weight?: number
    wheels?: string
    year?: string
}

@Module({ namespaced: true })
class CarList extends VuexModule {
    public cars?: Car[];
    public gg?: string = "test";
    @Mutation
    public setCars(cars: Car[]): void {
        console.log(cars);
        this.cars = cars
    }
    
    
    @Action({ rawError: true })
    public fetchCars(): void {
        fetch(this.context.rootState.SERVER_URL + '/cars')
        .then((response) => {
            if (response.status === 200){
                response.json()
                .then((data) => {
                    console.log(data);
                    this.context.commit('setCars', data as Car[])
                })
            }
        })

        
    }
}





export { CarList, Car}