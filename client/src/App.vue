<template>
    <div id="app">
         <Layout style="height:100vh">
            <Header style="display: flex; align-items: center; justify-content: center">
                <DatePicker type="date" placeholder="Select date" style="width: 200px" v-model="currentDateValue"></DatePicker>
                <NumberSelect v-model="currentPairValue" />
            </Header>
            <Content>
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
    @import "~iview/dist/styles/iview.css";
    @import "~tippy.js/index.css";

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
