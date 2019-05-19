<template>
    <div id="app">
        <el-container style="height:100vh">
            <el-header style="display: flex; align-items: center; justify-content: center">
                <el-date-picker
                        v-model="currentDateValue"
                        type="date"
                        placeholder="Pick a day">
                </el-date-picker>
                <el-pagination
                        :current-page.sync="currentPairValue"
                        background
                        layout="pager"
                        :pager-count=9
                        :total=80>
                </el-pagination>
                <el-switch
                        inactive-text="Занятые"
                        active-text="Свободные"
                >
                </el-switch>

            </el-header>
            <el-main style="padding: 0; overflow: hidden;">
                <building/>
            </el-main>
        </el-container>
    </div>
</template>

<script lang="ts">
    import {Component, Vue} from 'vue-property-decorator';
    import Building from './components/Building.vue';
    import {namespace} from "vuex-class"
    import ElementUI from 'element-ui';
    import * as locale from 'element-ui/lib/locale/lang/en';

    const Auditories = namespace("auditories");

    Vue.use(ElementUI, {locale});

    @Component({
        components: {
            Building,
        },
    })
    export default class App extends Vue {
        @Auditories.State("auditoriesOccupations") auditoriesOccupations: any;
        @Auditories.Action('fetchAuditories') fetchAuditories: any;
        @Auditories.Action('updateAuditoryOccupationDate') updateAuditoryOccupationDate: any;
        @Auditories.Mutation('setCurrentPair') setCurrentPair: any;
        @Auditories.State("currentDate") currentDate!: Date;
        @Auditories.State("currentPair") currentPair!: number;

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

        created() {
            this.fetchAuditories();
            this.updateAuditoryOccupationDate({date: new Date(2019, 5, 20)});
        }
    }
</script>

<style lang="scss">
    @import "~element-ui/lib/theme-chalk/index.css";
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
