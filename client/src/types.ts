import {Dictionary} from "vuex";

export interface RootState {

}

export enum AuditoriesStatisticsMode {
    Occupied = 'Занятые аудтиории',
    Free = 'Свободные аудитории',
}

export enum AuditoriesLevel {
    Basement = "Цоколь",
    First = "Первый",
    Second = "Второй",
    Third = "Третий",
}

export interface AuditoriesState {
    auditories: Dictionary<AuditoryItem>
    auditoriesOccupations: Dictionary<AuditoryOccupationItem>,
    currentDate: Date,
    currentPair: number,
    currentMode: AuditoriesStatisticsMode,
    currentLevel: number,
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
    teacher: string,
    discipline: string,
    kont: string,
    nt: number
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