import {Dictionary} from "vuex";

export interface RootState {

}

export interface AuditoriesState {
    auditories: Dictionary<AuditoryItem>
    auditoriesOccupations: Dictionary<AuditoryOccupationItem>,
    currentDate: Date,
    currentPair: number,
    showOccupied: boolean,
}

export interface AuditoryItem {
    id: number,
    key: string,
    title: string;
}

export interface OccupationItem {
    id: bigint,
}

export interface AuditoryOccupationItem {
    key: string;
    items: Array<OccupationItem>
}

export const LetterMapping: Dictionary<string> = {
    a: 'А',
    b: 'Б',
    v: 'В',
    g: 'Г',
    d: 'Д',
    e: 'Е',
    j: 'Ж',
    i: 'И',
    k: 'К',
};