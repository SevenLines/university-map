import Vue from 'vue'
import App from './App.vue'
import store from './store/index'

Vue.config.productionTip = false;

import Buefy from 'buefy';

Vue.use(Buefy, {
    defaultIconPack: 'fas',
});


new Vue({
    store,
    render: h => h(App)
}).$mount('#app');
