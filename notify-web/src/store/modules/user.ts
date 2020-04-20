// import { VuexModule, Module, Mutation, Action, } from 'vuex-module-decorators'

// @Module({ namespaced: true })
// class User extends VuexModule {
//     email?: string
//     group?: string
//     public gg?: string = "test";
//     @Mutation
//     public setCars(cars: Car[]): void {
//         this.cars = cars
//     }
    
    
//     @Action({ rawError: true })
//     public fetchCars(): void {
//         fetch(window.SERVER_URL + '/cars')
//         .then((response) => {
//             if (response.status === 200){
//                 response.json()
//                 .then((data) => {
//                     console.log(data);
//                     this.context.commit('setCars', data as Car[])
//                 })
//             }
//         })
//     }

//     @Action
//     public sortCars(sortFn: (a: Car, b: Car) => number): void {
//         const tmpCars = this.cars?.slice()
//         tmpCars?.sort(sortFn)
//         this.context.commit('setCars', tmpCars)
//     }
// }





// export { User}