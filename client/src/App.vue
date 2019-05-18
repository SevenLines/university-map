<template>
  <div id="app">
    <Floor/>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Floor from './components/Floor.vue';

@Component({
  components: {
    Floor,
  },
})
export default class App extends Vue {}
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
