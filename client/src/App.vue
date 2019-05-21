<template>
    <div id="app">
         <Layout style="height:100vh">
            <Header style="display: flex; align-items: center; justify-content: center">
                <Select v-model="modeValue" style="width:200px">
                    <Option v-for="mode in modes" :value="mode.key" :key="mode.key">{{ mode.value }}</Option>
                </Select>
                <DatePicker type="date" placeholder="Select date" style="width: 200px; margin-left: 1em"
                            v-model="currentDateValue"></DatePicker>
                <NumberSelect v-model="currentPairValue" />
            </Header>
            <Content style="position: relative">
                <div style="position: absolute; right: 1em; top: 1em;">
                    Этаж:
                    <Button v-for="level in levels"
                            :key="level.key"
                            @click="currentLevelValue = level.value"
                            :type="currentLevelValue == level.value ? 'primary': 'default'">{{level.key}}</Button>
                </div>
                <building/>
            </Content>
        </Layout>
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
            this.updateAuditoryOccupationDate({date: new Date(2019, 5, 20)});
        }
    }
</script>

<style lang="scss">
    @import "~iview/dist/styles/iview.css";
    @import "~tippy.js/index.css";
    @import "~animate.css/animate.css";

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
