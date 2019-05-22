<template>
    <div id="app" style="height: 100%;">
        <div style="display: flex; flex-direction: column; height: 100%">
            <div style="display: flex; padding: 0.5em 1em">
                <div style="display: flex">
                    <b-select placeholder="Select a name" v-model="modeValue">
                        <option
                                v-for="(mode, id) in modes"
                                :value="id"
                                :key="id">
                            {{ mode }}
                        </option>
                    </b-select>
                    <b-autocomplete
                            style="margin-left: 1em; width: 300px"
                            v-model="currentTeacherIdValue"
                            :keep-first="true"
                            :expanded="true"
                            :open-on-focus="true"
                            :data="teachersFilteredOrdered"
                             @input="onTeacherSelect"
                            :custom-formatter="i => i.fullName"
                            field="id">
                    </b-autocomplete>
                    <b-datepicker
                            style="margin-left: 1em"
                            v-model="currentDateValue"
                            placeholder="Click to select..."
                            icon="calendar-today">
                    </b-datepicker>
                </div>
                <div style="align-self: flex-end">
                    <NumberSelect v-model="currentPairValue"/>
                </div>
            </div>
            <div style="flex-grow: 1; position: relative; background-color: #f9f9f9">
                <div style="position: absolute; right: 1em; top: 1em;">
                    <b-button v-for="(level, id) in levels"
                              :key="id"
                              style="margin-right: 0.5em"
                              @click="currentLevelValue = id"
                              :type="currentLevelValue == id ? 'is-primary': ''">{{level}}
                    </b-button>
                </div>
                <building/>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
    import _ from 'lodash';
    import {Component, Vue} from 'vue-property-decorator';
    import Building from './components/Building.vue';
    import {namespace} from "vuex-class"
    import NumberSelect from "@/components/common/NumberSelect.vue"
    import {AuditoriesLevel, AuditoriesStatisticsMode, AuditoryItem, TeacherItem} from '@/types'
    import {Dictionary} from "vuex"

    const Auditories = namespace("auditories");

    @Component({
        components: {
            Building,
            NumberSelect,
        },
    })
    export default class App extends Vue {
        @Auditories.State("auditoriesOccupations") auditoriesOccupations: any;
        @Auditories.Action('fetchAuditories') fetchAuditories: any;
        @Auditories.Action('fetchTeachers') fetchTeachers: any;
        @Auditories.Action('updateAuditoryOccupationDate') updateAuditoryOccupationDate: any;
        @Auditories.Mutation('setCurrentPair') setCurrentPair: any;
        @Auditories.Mutation('setCurrentMode') setCurrentMode: any;
        @Auditories.Mutation('setCurrentLevel') setCurrentLevel: any;
        @Auditories.Mutation('setCurrentTeacherId') setCurrentTeacherId: any;
        @Auditories.State("currentDate") currentDate!: Date;
        @Auditories.State("currentPair") currentPair!: number;
        @Auditories.State("currentMode") currentMode!: AuditoriesStatisticsMode;
        @Auditories.State("currentLevel") currentLevel!: AuditoriesLevel;
        @Auditories.State("currentTeacherId") currentTeacherId!: number;
        @Auditories.State("teachers") teachers!: Dictionary<TeacherItem>;

        teacherFilter: string = "";

        get currentDateValue(): Date {
            return this.currentDate;
        }

        set currentDateValue(value) {
            this.updateAuditoryOccupationDate({date: value});
        }

        get currentPairValue(): number {
            return this.currentPair;
        }

        set currentPairValue(value) {
            this.setCurrentPair(value);
        }

        get modeValue(): AuditoriesStatisticsMode {
            return this.currentMode;
        }

        set modeValue(value) {
            this.setCurrentMode(value);
        }

        get currentLevelValue(): AuditoriesLevel {
            return this.currentLevel;
        }

        set currentLevelValue(value: AuditoriesLevel) {
            this.setCurrentLevel(value);
        }

        get currentTeacherIdValue(): number {
            return this.currentTeacherId;
        }

        set currentTeacherIdValue(value: number) {
            this.setCurrentTeacherId(value);
        }

        get modes() {
            return {
                [AuditoriesStatisticsMode.Occupied]: 'Занятые',
                [AuditoriesStatisticsMode.Free]: 'Свободные',
                [AuditoriesStatisticsMode.ByTeacher]: 'По преподавателю',
            }
        }

        get levels() {
            return {
                [AuditoriesLevel.Basement]: 'Цоколь',
                [AuditoriesLevel.First]: 'Первый',
                [AuditoriesLevel.Second]: 'Второй',
                [AuditoriesLevel.Third]: 'Третий',
            }
        }

        get teachersFilteredOrdered() {
            return _(this.teachers).filter(i => {
                return !this.teacherFilter || i.fullName.includes(this.teacherFilter)
            }).sortBy(i => i.fullName).value();
        }

        created() {
            this.fetchAuditories();
            this.fetchTeachers();
            this.updateAuditoryOccupationDate({date: new Date()});
        }

        onTeacherSelect(option: any) {
            console.log(arguments);
            this.teacherFilter = option;
        }
    }
</script>

<style lang="scss">
    /*@import "~iview/dist/styles/iview.css";*/
    @import "~tippy.js/index.css";
    @import "~animate.css/animate.css";
    @import '~buefy/dist/buefy.css';


    body {
        margin: 0;
        padding: 0;
    }

    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
    }


</style>
