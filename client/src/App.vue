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
              style="margin-left: 1em; width: 550px"
              v-if="teacherSelectorVisible"
              v-model="currentTeacherIdValue"
              :options="teachersOrdered"
              label="fullName"
              placeholder="Select teacher">
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
                    :type="currentLevelValue == id ? 'is-primary': ''">
            {{level}}
          </b-button>
        </div>
        <building/>
        <div class="statistics-window">
          <div style="height: 3em; margin-bottom: 0.5em; margin-top: 0.5em">
            <h2>Статистика по аудитории</h2>
            <div v-if="clickedAuditory">
              {{ clickedAuditory.title }}
            </div>
          </div>
          <section>
            <button class="button is-primary is-medium"
                    @click="isModalActive = true">
              Показать статистику
            </button>
            <b-modal :active.sync="isModalActive" :width="1000" scroll="keep">
              <div class="card">
                <div class="card-content">
                  <div class="media">
                    <div class="media-left">
                      <div ref="graph" style="height: 400px; width: 450px"></div>
                    </div>
                    <div class="media-right">
                      <div ref="graph2" style="height: 400px; width: 450px"></div>
                    </div>
                  </div>
                  <div class="content">
                    <div ref="graph3" style="height: 400px; width: 450px"></div>
                  </div>
                  <button class="button is-primary is-medium"
                          @click="isModalActive = false">
                    Назад
                  </button>
                </div>
              </div>
            </b-modal>
          </section>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
    import _ from 'lodash';
    import {Component, Vue, Watch} from 'vue-property-decorator';
    import Building from './components/Building.vue';
    import {namespace} from "vuex-class"
    import NumberSelect from "@/components/common/NumberSelect.vue"
    import {AuditoriesLevel, AuditoriesStatisticsMode, AuditoryItem, TeacherItem, AuditoryStatisticsView} from '@/types'
    import {Dictionary} from "vuex"
    import EventBus from "@/utils/event_bus";
    import axios from 'axios';
    import echarts from 'echarts';
    import chroma from 'chroma-js';

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

        clickedAuditory: AuditoryItem | null = null
        AuditoryStatisticPair: any = {}
        AuditoryStatisticDay: any = {}
        AuditoryStatisticDayExt: any = {}
        isModalActive: boolean = false

        @Watch("isModalActive")
        onIsModalActive() {
            if (this.isModalActive) {
                this.$nextTick(() => {
                    let chart = echarts.init(this.$refs.graph as any)
                    chart.setOption(this.chartPara)
                    let chart2 = echarts.init(this.$refs.graph2 as any)
                    chart2.setOption(this.chartDay)
                    let chart3 = echarts.init(this.$refs.graph3 as any)
                    chart3.setOption(this.chartDayExt)
                })
            }
        }

        get chartPara(): any {
            return {
                title: {
                    text: 'Статистика по парам'
                },
                xAxis: {
                    data: ['1', '2', '3', '4', '5', '6', '7', '8'],
                    name: "Пара",
                    nameLocation: 'middle',
                    nameGap: '35'
                },
                yAxis: {
                    type: 'value',
                    name: "%",
                    position: 'left',
                    nameLocation: 'middle',
                    nameGap: '25'
                },
                series: [{
                    data: _.map([0, 1, 2, 3, 4, 5, 6, 7], (i: any) => {
                        let value = this.AuditoryStatisticPair[i] ? this.AuditoryStatisticPair[i].percentage : 0
                        let f = chroma.scale(['lightgreen', 'orange', 'red']).domain([0, 50, 100])
                        return {
                            value: value,
                            itemStyle: {color: f(Number(value)).hex()}
                        }
                    }),
                    type: 'bar'
                }]
            }
        }

        get chartDay(): any {
            return {
                title: {
                    text: 'Статистика по дням',
                },
                xAxis: {
                    data: ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
                    name: "День",
                    nameLocation: 'middle',
                    nameGap: '35',
                    axisLabel: {
                        rotate: 90
                    }
                },
                yAxis: {
                    type: 'value',
                    name: "%",
                    position: 'left',
                    nameLocation: 'middle',
                    nameGap: '25',
                },
                series: [{
                    data: _.map([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], (i: any) => {
                        let value = this.AuditoryStatisticDay[i] ? this.AuditoryStatisticDay[i].percentage : 0
                        let f = chroma.scale(['lightgreen', 'orange', 'red']).domain([0, 50, 100])
                        return {
                            value: value,
                            itemStyle: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                    offset: 0,
                                    color: f(Number(value)).hex()
                                }, {
                                    offset: 1,
                                    color: 'lightgreen'
                                }])
                            }
                        }
                    }),
                    type: 'bar'
                }]
            }
        }
// Календарь
        get chartDayExt(): any {
            console.log(this.AuditoryStatisticDayExt)  // ??? Не получается достать дату T.T
            return {
                visualMap: {
                    show: false,
                    min: 0,
                    max: 300,
                    calculable: true,
                    seriesIndex: [2],
                    orient: 'horizontal',
                    left: 'center',
                    bottom: 20,
                    inRange: {
                        color: ['#e0ffff', '#006edd'],
                        opacity: 0.3
                    },
                    controller: {
                        inRange: {
                            opacity: 0.5
                        }
                    }
                },
                calendar: [{
                    left: 'center',
                    top: 'middle',
                    cellSize: [70, 70],
                    yearLabel: {show: true},
                    orient: 'vertical',
                    dayLabel: {
                        firstDay: 1,
                        nameMap: 'en'
                    },
                    monthLabel: {
                        show: true
                    },
                    range: '2018-06'
                }],
                series: [{
                    type: 'scatter',
                    coordinateSystem: 'calendar',
                    symbolSize: 1,
                    data: 1
                }, {
                    type: 'scatter',
                    coordinateSystem: 'calendar',
                    symbolSize: 1,
                    data: 1
                }, {
                    name: '降雨量',
                    type: 'heatmap',
                    coordinateSystem: 'calendar',
                    data: 1
                }]
            }
        }

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

        get ViewStyle() {
            return {
                [AuditoryStatisticsView.para]: "По паре",
                [AuditoryStatisticsView.day]: "По дню",
            }
        }

        created() {
            this.fetchAuditories();
            this.fetchTeachers();
            this.updateAuditoryOccupationDate({date: new Date()});

            EventBus.$on("auditoryClicked", this.onAuditoryClicked)
        }

        onAuditoryClicked(data: any) {
            axios.get("/api/auditories/statistic-para", {
                params: {
                    auditory_id: data.auditory.id,
                }
            }).then(r => {
                this.AuditoryStatisticPair = r.data
            })

            axios.get("/api/auditories/statistic-day", {
                params: {
                    auditory_id: data.auditory.id,
                }
            }).then(r => {
                this.AuditoryStatisticDay = r.data
            })

            axios.get("/api/auditories/statistic-ext", {
                params: {
                    auditory_id: data.auditory.id
                }
            }).then(r => {
                this.AuditoryStatisticDayExt = r.data
            })

            this.clickedAuditory = data.auditory
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
