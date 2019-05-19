import {AuditoriesState, RootState} from "@/types";
import {Module} from "vuex";
import {actions} from "@/store/auditories/actions";
import {mutations} from "@/store/auditories/mutations";


export const auditories: Module<AuditoriesState, RootState> = {
    namespaced: true,
    state: {
        auditories: {},
        auditoriesOccupations: {},
        date: new Date()
    },
    actions,
    mutations,
};