import {ActionTree} from "vuex";
import {AuditoriesState, RootState} from "@/types";
import axios from 'axios';
import moment from 'moment';
import {URL_AUDITORIES_LIST, URL_DAY_AUDITORY_OCCUPATION} from "@/urls";
import {DATE_FORMAT} from "@/consts";

export const actions: ActionTree<AuditoriesState, RootState> = {
    updateAuditoryOccupationDate({commit}, {date}): any {
        axios.get(URL_DAY_AUDITORY_OCCUPATION, {
            params: {
                date: moment(date).format(DATE_FORMAT)
            }
        }).then(r => {
            commit('setCurrentDate', date);
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