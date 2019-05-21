<template :src="`template/${template}`">
    
</template>

<script lang="ts">
 import {Component, Prop, Vue} from 'vue-property-decorator';

    @Component({})
    export default class FloorBase extends Vue {
        protected template!: string;

        mounted() {

        }
    }
</script>

<style scoped>

</style>