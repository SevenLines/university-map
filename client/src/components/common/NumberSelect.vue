<template>
    <div class="pair-selector">
        <div class="pair-selector-item" v-for="i in count" :class="klass(i)" @click="handleClick(i)">
            {{i}}
        </div>
    </div>
</template>

<script lang="ts">
    import {Component, Prop, Vue, Watch} from 'vue-property-decorator'

  @Component
  export default class NumberSelect extends Vue {
        @Prop() private value!: number;
        @Prop({default: 8}) private count!: number;
        private number: number = this.value;

        @Watch('number')
        onNumberChanged() {
            this.$emit('input', this.number);
        }

        handleClick(value: number) {
            this.number = value;
        }

        klass(i: number): any {
            return {
                'selected': i == this.number
            }
        }
  }
</script>

<style scoped lang="scss">
    $selectedColor: #ffdb2d;
    .pair-selector {
        display: flex;
        padding-left: 1em;

        .pair-selector-item {
            cursor: pointer;
            line-height: normal;
            background-color: white;
            padding: 0.5em 1em;

            &.selected {
                background-color: $selectedColor;
                color:  white;
                box-shadow: 0 0 0 2px darken($selectedColor, 10) inset;
            }

            &:hover {
                background-color: $selectedColor;
                color: white;
            }
        }
    }
</style>