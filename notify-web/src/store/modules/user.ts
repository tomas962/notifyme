import { VuexModule, Module, Mutation, Action, } from 'vuex-module-decorators'
import JWT from 'jwt-decode'

class Identity {
    email = "";
    group = "";
    user_id = -1;

}

interface UserState
{
    identity: Identity; 
    access_token?: string; 
    refresh_token?: string;
}

@Module({ namespaced: true })
class User extends VuexModule {
    identity: Identity = new Identity();
    access_token = "";
    refresh_token = "";
    @Mutation
    public updateUser(state: UserState) {
        this.identity = state.identity;
        this.access_token = state.access_token ? state.access_token : "";
        this.refresh_token = state.refresh_token ? state.refresh_token : "";
        console.log("MUTATIOn");
        
    }

    @Action
    setUser(state: UserState) {
        console.log("ACTION");
        this.context.commit('updateUser', state)
    }

    @Action
    watchToken() {
        const timestamp = (Date.now() / 1000) | 0;
        const decoded_token: any = JWT(this.access_token)
        setTimeout(() => {
            console.log("LOGGING OUT USER");
            
        }, decoded_token.exp - timestamp)
    }

}





export { User, Identity, UserState}