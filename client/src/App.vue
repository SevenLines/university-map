<template>
    <div id="app">
        <building/>
    </div>
</template>

<script lang="ts">
    import {Component, Vue} from 'vue-property-decorator';
    import Building from './components/Building.vue';
    import {namespace} from "vuex-class"

    const Auditories = namespace("auditories");

    @Component({
        components: {
            Building,
        },
    })
    export default class App extends Vue {
        @Auditories.State("auditoriesOccupations") auditoriesOccupations: any;
        @Auditories.Action('fetchAuditories') fetchAuditories: any;
        @Auditories.Action('updateAuditoryOccupationDate') updateAuditoryOccupationDate: any;

        created() {
            this.fetchAuditories();
            this.updateAuditoryOccupationDate({date: new Date(2019, 5, 20)});
        }
    }
</script>

<style lang="scss">
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
