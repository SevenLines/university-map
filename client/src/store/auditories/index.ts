import {AuditoriesLevel, AuditoriesState, AuditoriesStatisticsMode, RootState} from "@/types";
import {Module} from "vuex";
import {actions} from "@/store/auditories/actions";
import {mutations} from "@/store/auditories/mutations";


export const auditories: Module<AuditoriesState, RootState> = {
    namespaced: true,
    state: {
        auditories: {},
        auditoriesOccupations: {},
        currentDate: new Date(),
        showOccupied: true,
        currentPair: 1,
        currentMode: AuditoriesStatisticsMode.Occupied,
        currentLevel: 1,
    },
    actions,
    mutations,
};