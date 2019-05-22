import {ActionTree} from "vuex";
import {AuditoriesState, RootState} from "@/types";
import axios from 'axios';
import moment from 'moment';
import {URL_AUDITORIES_LIST, URL_DAY_AUDITORY_OCCUPATION, URL_TEACHER_OCCUPATION, URL_TEACHERS_LIST} from "@/urls";
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
    },
    updateTeacherOccupation({commit}, {teacher_id}): any {
        axios.get(URL_TEACHER_OCCUPATION, {
            params: {
                id: teacher_id
            }
        }).then(r => {
            commit('setTeacherId', teacher_id);
            commit('setTeacherOccupation', r.data)
        })
    },
    fetchTeachers({commit}): any {
        axios.get(URL_TEACHERS_LIST, {
            params: {}
        }).then(r => {
            commit('setTeachers', r.data)
        })
    }
};