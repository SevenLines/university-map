<template src="./templates/floor0.html"></template>

<script lang="ts">
    import {Component, Prop, Vue} from 'vue-property-decorator';
    import FloorBase from "@/components/FloorBase.vue"
    import Auditory from "@/components/Auditory.vue"

    @Component({
        components: {
            Auditory
        }
    })
    export default class Floor0 extends FloorBase {
        mounted() {

        }
    }
</script>

<style scoped lang="scss">

</style>