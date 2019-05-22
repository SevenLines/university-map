import {Dictionary} from "vuex";

export interface RootState {

}

export enum AuditoriesStatisticsMode {
    Occupied,
    Free,
    ByTeacher,
}

export enum AuditoriesLevel {
    Basement,
    First,
    Second,
    Third,
}

export interface AuditoriesState {
    auditories: Dictionary<AuditoryItem>
    teachers: Dictionary<TeacherItem>
    auditoriesOccupations: Dictionary<AuditoryOccupationItem>,
    teacherOccupation: Array<TeacherOccupationItem>
    currentDate: Date,
    currentPair: number,
    currentMode: AuditoriesStatisticsMode,
    currentLevel: number,
    currentTeacherId: number | null,
    showOccupied: boolean,
}

export interface AuditoryItem {
    id: number,
    key: string,
    title: string;
}

export interface TeacherItem {
    id: number,
    name: string,
    fullName: string,
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

export interface TeacherOccupationItem {
    para: number,
    everyweek: number,
    day: number,
    aud_id: number,
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