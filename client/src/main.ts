import Vue from 'vue'
import App from './App.vue'
import store from './store/index'
import vSelect from 'vue-select';


Vue.config.productionTip = false;

import Buefy from 'buefy';

Vue.use(Buefy, {
    defaultIconPack: 'fas',
});

import Multiselect from 'vue-multiselect'

// register globally
Vue.component('multiselect', Multiselect)

Vue.component('v-select', vSelect);

new Vue({
    store,
    render: h => h(App)
}).$mount('#app');
