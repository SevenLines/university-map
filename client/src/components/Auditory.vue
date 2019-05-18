<template>

</template>

<script lang="ts">
    import {Component, Prop, Vue} from 'vue-property-decorator';

    @Component({})
    export default class Auditory extends Vue {
        @Prop() private d!: string;
        @Prop() private width!: number;
    }
</script>

<style scoped>

</style>