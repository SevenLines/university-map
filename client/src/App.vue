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
                    <multiselect
                            style="margin-left: 1em; width: 400px"
                            v-if="teacherSelectorVisible"
                            v-model="currentTeacherIdValue"
                            :options="teachersOrdered"
                            label="fullName"
                    >
                    </multiselect>
                    <b-datepicker
                            style="margin-left: 1em"
                            v-if="dateIsVisible"
                            v-model="currentDateValue"
                            placeholder="Click to select..."
                            icon="calendar-today">
                    </b-datepicker>
                </div>
                <div style="align-self: flex-end" v-if="pairsSelectorVisible">
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
                <div class="statistics-window">
                    <h2>Статистика по аудитории</h2>
                    <div v-if="clickedAuditory">
                        <!-- выводить статистику сюда -->
                        {{ clickedAuditory.title }}
                    </div>
                    <div v-for="items in AuditoryStatistic">
                        {{ items.para }} {{ items.count }} {{ items.percentage }}
                    </div>
                    <div ref="graph" style="height: 300px"></div>
                </div>
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
    import EventBus from "@/utils/event_bus";
    import axios from 'axios';
    import echarts from 'echarts';

    EventBus.$off();

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
        @Auditories.Action('updateTeacherOccupation') updateTeacherOccupation: any;
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

        clickedAuditory: AuditoryItem | null = null;
        AuditoryStatistic: any = {};
        chart: any = null;

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
            this.setCurrentMode(Number(value));
        }

        get currentLevelValue(): AuditoriesLevel {
            return this.currentLevel;
        }

        set currentLevelValue(value: AuditoriesLevel) {
            this.setCurrentLevel(value);
        }

        get currentTeacherIdValue(): any {
            return this.currentTeacherId;
        }

        set currentTeacherIdValue(value) {
            this.updateTeacherOccupation({teacher_id: value.id});
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

        get teachersOrdered() {
            return _(this.teachers).sortBy(i => i.fullName).value();
        }

        get teacherSelectorVisible() {
            return this.currentMode == AuditoriesStatisticsMode.ByTeacher
        }

        get dateIsVisible() {
            return this.currentMode != AuditoriesStatisticsMode.ByTeacher
        }

        get pairsSelectorVisible() {
            return this.currentMode != AuditoriesStatisticsMode.ByTeacher
        }

        created() {
            this.fetchAuditories();
            this.fetchTeachers();
            this.updateAuditoryOccupationDate({date: new Date()});

            // слушаем событие auditoryClicked, подключаем к нему обработчик onAuditoryClicked
            EventBus.$on("auditoryClicked", this.onAuditoryClicked)
        }

        mounted() {
            this.chart = echarts.init(this.$refs.graph as any);
            this.chart.setOption({
                xAxis: {
                    type: 'category',
                    data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                },
                yAxis: {
                    type: 'value'
                },
                series: [{
                    data: [820, 932, 901, 934, 1290, 1330, 1320],
                    type: 'bar'
                }]
            });
        }

        // метода который будет вызываться по событию auditoryClicked
        // так как тут используется TypeScript то надо указывать тип,
        // чтобы не мучаться с типами можно просто указывать any
        onAuditoryClicked(data: any) {
            axios.get("/api/auditories/statistic", {
                params: {
                    auditory_id: data.auditory.id,
                }
            }).then(r => {
                console.log(r.data)
                console.log(r.data[0].count)
                console.log(r.data[0].para)
                this.AuditoryStatistic = r.data
            })
            console.log(data)
            // чтобы вывести в консоли содержимое data
            if (data.auditory) {
                // вывод алерта
                alert(`Hello auditory ${data.id} with database id=${data.auditory.id} and name=${data.auditory.title}`);
            }
        }

        onTeacherSelect(option: any) {
            this.teacherFilter = option;
        }
    }
</script>


<style lang="scss">
    /*@import "~iview/dist/styles/iview.css";*/
    @import "~tippy.js/index.css";
    @import "~animate.css/animate.css";
    @import '~buefy/dist/buefy.css';
    @import '~vue-multiselect/dist/vue-multiselect.min.css';


    body {
        margin: 0;
        padding: 0;
    }

    .statistics-window {
        position: absolute;
        left: 1em;
        top: 1em;
        padding: 1em;
        background-color: white;
    }

    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
    }

    .vs__selected {
        white-space: nowrap;
        max-width: 100px;
        text-overflow: ellipsis;
    }


</style>
