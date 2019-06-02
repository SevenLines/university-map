<template>
    <div style="height: 100%">
        <svg ref="svg" width="100%" height="100%">
            <Floor0 :key="0" style="transform: translate(0, 0)" :class="floorClass(0)"/>
            <Floor1 :key="1" style="transform: translate(2px, -8px)" :class="floorClass(1)"/>
            <Floor2 :key="2" style="transform: translate(4px, -16px)" :class="floorClass(2)"/>
            <Floor3 :key="3" style="transform: translate(6px, -24px)" :class="floorClass(3)"/>
        </svg>
    </div>
</template>

<script lang="ts">
    import {Component, Prop, Vue, Watch} from 'vue-property-decorator';
    import svgPanZoom from 'svg-pan-zoom';
    import Floor0 from "@/components/Floor0.vue"
    import Floor1 from "@/components/Floor1.vue";
    import Floor2 from "@/components/Floor2.vue"
    import Floor3 from "@/components/Floor3.vue"
    import NumberSelect from "@/components/common/NumberSelect.vue"
    import {namespace} from "vuex-class"

    const Auditories = namespace("auditories");

    @Component({
        components: {
            Floor0,
            Floor1,
            Floor2,
            Floor3,
            NumberSelect,
        }
    })
    export default class Building extends Vue {
        @Auditories.State("currentLevel") currentLevel!: number;

        private panZoomTiger!: SvgPanZoom.Instance;
        private floors = ['Floor1', 'Floor2', 'Floor3'];


        mounted() {
            this.panZoomTiger = svgPanZoom(<HTMLElement>this.$refs.svg, {
                zoomScaleSensitivity: 1,
                minZoom: 0.5,
                maxZoom: 10
            });
        }

        floorClass(index: number) {
            return {
                'hidden': index - this.currentLevel >= 1,
                'semi-visible': index != this.currentLevel
            }
        }
    }
</script>

<style lang="scss">
    rect, path {
        fill: transparent;
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

    .hidden {
        display: none;
    }

    .semi-visible {
        opacity: 0.15;
    }
</style>
