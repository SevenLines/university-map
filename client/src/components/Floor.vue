<template>
    <div class="content">
        <svg ref="svg" width="100%" height="900px" fill-rule="evenodd" version="1.1"
             xmlns="http://www.w3.org/2000/svg">
            <Floor1 ref="floor1"/>
        </svg>
    </div>
</template>

<script lang="ts">
    import {Component, Prop, Vue} from 'vue-property-decorator';
    import svgPanZoom from 'svg-pan-zoom';
    import Floor1 from './Floor1.vue';

    @Component({
        components: {
            Floor1
        }
    })
    export default class Floor extends Vue {
        @Prop() private msg!: string;

        mounted() {
            let panZoomTiger = svgPanZoom(<HTMLElement>this.$refs.svg, {
                zoomScaleSensitivity: 1
                , minZoom: 1
                , maxZoom: 10
            });
        }
    }
</script>

<style lang="scss">
    rect, path {
        /*fill: white;*/
        stroke: #848484;
        stroke-width: 0.2px;
    }
    text {
        stroke: none;
        fill: black;
    }
</style>
