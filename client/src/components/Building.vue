<template>
    <div class="content" style="height: 99vh">
        <svg ref="svg" width="100%" height="100%">
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
    export default class Building extends Vue {
        private panZoomTiger!: SvgPanZoom.Instance;

        mounted() {
            this.panZoomTiger = svgPanZoom(<HTMLElement>this.$refs.svg, {
                zoomScaleSensitivity: 1,
                minZoom: 1,
                maxZoom: 10
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
    #way {
        fill: #fff6e6;
    }
</style>
