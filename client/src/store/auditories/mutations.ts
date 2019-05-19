import _ from 'lodash';
import {MutationTree} from "vuex";
import {AuditoriesState, AuditoryItem, AuditoryOccupationItem, RootState} from "@/types";

export const mutations: MutationTree<AuditoriesState> = {
    setAuditoriesOccupation(state, payload) {
        state.auditoriesOccupations = payload;
    },
    setAuditories(state, payload) {
        state.auditories = _(payload).map<AuditoryItem>(i => ({
                id: i.id,
                key: i.key,
                title: i.title,
            })
        ).keyBy(i => i.key).value();
    },
    setCurrentDate(state, date: Date) {
        state.currentDate = date;
    }
};