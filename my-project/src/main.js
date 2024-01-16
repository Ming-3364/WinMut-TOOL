import Vue from 'vue'
import axios from 'axios';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue'

axios.defaults.baseURL = 'http://localhost:5000';  // Flask应用的地址
Vue.prototype.$axios = axios;

Vue.use(ElementUI);


Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
