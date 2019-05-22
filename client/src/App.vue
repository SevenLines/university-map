<template>
    <div id="app" style="height: 100%;">
        <div style="display: flex; flex-direction: column; height: 100%">
            <div style="display: flex; padding: 0.5em 1em">
                <div style="display: flex">
                    <b-select placeholder="Select a name" v-model="modeValue">
                        <option
                                v-for="mode in modes"
                                :value="mode.key"
                                :key="mode.key">
                            {{ mode.value }}
                        </option>
                    </b-select>
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
                    <b-button v-for="level in levels"
                              :key="level.key"
                              style="margin-right: 0.5em"
                              @click="currentLevelValue = level.value"
                              :type="currentLevelValue == level.value ? 'is-primary': ''">{{level.key}}
                    </b-button>
                </div>
                <building/>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
    import {Component, Vue} from 'vue-property-decorator';
    import Building from './components/Building.vue';
    import {namespace} from "vuex-class"
    import NumberSelect from "@/components/common/NumberSelect.vue"
    import {AuditoriesLevel, AuditoriesStatisticsMode} from '@/types'

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
        @Auditories.Action('updateAuditoryOccupationDate') updateAuditoryOccupationDate: any;
        @Auditories.Mutation('setCurrentPair') setCurrentPair: any;
        @Auditories.Mutation('setCurrentMode') setCurrentMode: any;
        @Auditories.Mutation('setCurrentLevel') setCurrentLevel: any;
        @Auditories.State("currentDate") currentDate!: Date;
        @Auditories.State("currentPair") currentPair!: number;
        @Auditories.State("currentMode") currentMode!: AuditoriesStatisticsMode;
        @Auditories.State("currentLevel") currentLevel!: AuditoriesLevel;

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

        get modes() {
            return Object.keys(AuditoriesStatisticsMode).map(key => ({
                key,
                value: AuditoriesStatisticsMode[key as any]
            }));
        }

        get levels() {
            return [
                {key: "Цоколь", value: 0},
                {key: "Первый", value: 1},
                {key: "Второй", value: 2},
                {key: "Третий", value: 3},
            ]
        }

        created() {
            this.fetchAuditories();
            this.updateAuditoryOccupationDate({date: new Date()});
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
