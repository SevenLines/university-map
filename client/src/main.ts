import Vue from 'vue'
import App from './App.vue'
import store from './store/index'

import iView from 'iview';
import locale from 'iview/dist/locale/ru-RU';

Vue.config.productionTip = false;

Vue.use(iView, {locale});


new Vue({
    store,
    render: h => h(App)
}).$mount('#app');
