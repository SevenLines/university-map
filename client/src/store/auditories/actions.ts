import {ActionTree} from "vuex";
import {AuditoriesState, RootState} from "@/types";
import axios from 'axios';
import {URL_AUDITORIES_LIST, URL_DAY_AUDITORY_OCCUPATION} from "@/urls";

export const actions: ActionTree<AuditoriesState, RootState> = {
    fetchDayOccupation({commit}): any {
        axios.get(URL_DAY_AUDITORY_OCCUPATION, {
            params: {}
        }).then(r => {
            commit('setAuditoriesOccupation', r.data)
        })
    },
    fetchAuditories({commit}): any {
        axios.get(URL_AUDITORIES_LIST, {
            params: {}
        }).then(r => {
            commit('setAuditories', r.data)
        })
    }
};