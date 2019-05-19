import _ from 'lodash';
import {MutationTree} from "vuex";
import {AuditoriesState, Auditory, AuditoryOccupationItem, RootState} from "@/types";

export const mutations: MutationTree<AuditoriesState> = {
    setAuditoriesOccupation(state, payload) {
        state.auditoriesOccupations = _(payload).map<AuditoryOccupationItem>(i => ({
                items: i.items,
                key: i.key,
            })
        ).keyBy(i => i.key).value();
    },
    setAuditories(state, payload) {
        state.auditories = _(payload).map<Auditory>(i => ({
                id: i.id,
                key: i.key,
                title: i.title,
            })
        ).keyBy(i => i.key).value();
    },
    setDay(state, date: Date) {
        state.date = date;
    }
};