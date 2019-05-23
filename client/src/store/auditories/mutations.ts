import _ from 'lodash';
import {MutationTree} from "vuex";
import {AuditoriesLevel, AuditoriesState, AuditoriesStatisticsMode, AuditoryItem, TeacherItem} from "@/types";

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
    setTeachers(state, payload) {
        state.teachers = _(payload).map<TeacherItem>(i => ({
                id: i.id,
                name: i.name,
                fullName: i.full_name,
            })
        ).keyBy(i => i.id).value();
    },
    setTeacherOccupation(state, payload) {
        state.teacherOccupation = _(payload).groupBy(i => i.aud_id).value();
    },
    setCurrentDate(state, date: Date) {
        state.currentDate = date;
    },
    setCurrentPair(state, pair: number) {
        state.currentPair = pair;
    },
    setCurrentMode(state, mode: AuditoriesStatisticsMode) {
        state.currentMode = mode;
    },
    setCurrentLevel(state, level: number) {
        state.currentLevel = level;
    },
    setCurrentTeacherId(state, id: number) {
        state.currentTeacherId = id;
    }
};