import Vue from 'vue'
import Vuex, {StoreOptions} from 'vuex'
import {RootState} from "@/types";
import {auditories} from "@/store/auditories";

Vue.use(Vuex);


const store: StoreOptions<RootState> = {
  modules: {
    auditories
  }
};

export default new Vuex.Store(store)
