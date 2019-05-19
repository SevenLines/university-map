<template>
    <g class="auditory" :class="addClasses">
        <component class="border" :is="type" :d="d" :width="width" :height="height" :x="x" :y="y" ref="border"/>
        <text :x="textCenter.x" :y="textCenter.y">
            {{auditoryName}}
        </text>
    </g>
</template>

<script lang="ts">
    import {Component, Prop, Watch, Vue} from 'vue-property-decorator';
    import {Dictionary} from 'lodash';
    import {State, namespace} from 'vuex-class';
    import {AuditoryItem, AuditoryOccupationItem, LetterMapping} from "@/types"

    const Auditories = namespace("auditories");

    interface Point {
        x: number;
        y: number;
    }

    @Component
    export default class Auditory extends Vue {
        @Prop() private d!: string;
        @Prop() private width!: string;
        @Prop() private height!: string;
        @Prop() private x!: string;
        @Prop() private y!: string;
        @Prop() private id!: string;

        @Auditories.State("auditoriesOccupations") auditoriesOccupations: any;
        @Auditories.State("auditories") auditories: any;

        private toggleCenterUpdate: boolean = true;

        @Watch('d', {immediate: true})
        onDChanged() {
            this.$nextTick(() => {
                this.toggleCenterUpdate = !this.toggleCenterUpdate;
            })
        }

        get type(): string {
            return this.d ? "path" : "rect";
        }

        get auditory(): AuditoryItem | null {
            return this.auditories[this.audId];
        }

        get auditoryOccupation(): AuditoryOccupationItem | null {
            return this.auditory ? this.auditoriesOccupations[this.auditory.id] : null;
        }

        get regexMatch(): RegExpExecArray | null {
            let r = /aud-([abvgdejik])(\d{3})(\w?)/;
            return r.exec(this.id);
        }

        get audId(): string {
            return this.regexMatch ? this.regexMatch[1] + this.regexMatch[2] + this.regexMatch[3] : "";
        }

        get korpus(): string | null {
            if (this.regexMatch)
                return this.regexMatch[1];
            return null;
        }

        get addClasses(): Dictionary<boolean> {
            let klass: Dictionary<boolean> = {};
            if (this.korpus ) {
                klass[`korpus${this.korpus.toUpperCase()}`] = true;
            }
            klass['used-in-schedule'] = this.usedInSchedule;
            klass['is-occupied'] = this.isOccupied;
            return klass
        }

        get usedInSchedule() : boolean {
            return !!this.auditory;
        }

        get isOccupied(): boolean {
            return !!this.auditoryOccupation;
        }

        get auditoryName(): string {
            if (this.auditory) {
                return this.auditory ? this.auditory.title : "";

            } else {
                let match = this.regexMatch;
                if (match) {
                    let auditory = match[2];
                    let korpus = this.korpus ? LetterMapping[this.korpus] : "";
                    let letter = match[3] ? LetterMapping[match[3]] : '';
                    return `${korpus}${auditory}${letter.toLowerCase()}`;
                }
                return "";
            }
        }

        get textCenter(): Point {
            let out = {x: 0, y: 0};
            this.toggleCenterUpdate;
            if (this.type === 'rect') {
                out = {
                    x: parseFloat(this.x) + parseFloat(this.width) / 2,
                    y: parseFloat(this.y) + parseFloat(this.height) / 2,
                };
            } else {
                if (this.$refs.border) {
                    let bbox = (this.$refs.border as SVGAElement).getBBox();
                    out = {
                        x: bbox.x + bbox.width / 2,
                        y: bbox.y + bbox.height / 2,
                    }
                }
            }
            return out;
        }
    }
</script>

<style scoped lang="scss">
    $korpuses: "A", "B", "V", "G", "D", "E", "J", "I", "K";
    $korpusColors: #ffa698, #ffa2c8, #f7b0ff, #c1c6ff,
    #b7f8ff, #b7ffd6, #e1ff77, #fff4b0,
    #ffd884;

    .auditory {
        &.used-in-schedule {
            cursor: pointer;
        }

        text {
            text-anchor: middle;
            dominant-baseline: middle;
            font-size: 2px;
        }

        .border {
            -webkit-transition: all .3s;
            -moz-transition: all .3s;
            -ms-transition: all .3s;
            -o-transition: all .3s;
            transition: all .3s;
            fill: white;
            stroke-width: 0.25px;
            stroke: silver;


        }

        @for $i from 1 through length($korpuses) {
            $korpus: nth($korpuses, $i);
            $korpusColor: nth($korpusColors, $i);
            $borderFillColor: lighten($korpusColor, 10);
            $borderStokeColor: desaturate(darken($korpusColor, 40), 50);
            &.korpus#{$korpus} {
                &.used-in-schedule {
                    text {
                        /*stroke: desaturate(darken($korpusColor, 40), 50);
                        stroke-width: 0.1px;*/
                        fill: desaturate(darken($korpusColor, 70), 50);
                        font-weight: bold;
                        font-size: 2px;
                    }

                    .border {
                        fill: $borderFillColor;
                        stroke: $borderStokeColor;
                    }

                    &:hover {
                        .border {
                            fill: $korpusColor
                        }
                    }
                }
                &.is-occupied  {
                    .border {
                        stroke-width: 0.5px;
                        stroke: mix($borderStokeColor, red);
                        fill: darken($borderFillColor, 10);
                    }
                    &:hover {
                        .border {
                            fill: darken($korpusColor, 10);
                        }
                    }
                    text {
                        font-size: 3px;
                    }
                }
            }
        }


    }
</style>