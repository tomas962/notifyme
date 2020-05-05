import { VuexModule, Module, Mutation, Action, } from 'vuex-module-decorators'

@Module({ namespaced: true })
class UIState extends VuexModule {
    carAdsPage = 1
    @Mutation
    public updatePage(state: {page: number}) {
        console.log('update page mutation');
        
        this.carAdsPage = state.page
        console.log(this.carAdsPage);
    }

    @Action
    setPage(state: {page: number}) {
        console.log('update page action');
        this.context.commit('updatePage', state)
    }

}


export { UIState }