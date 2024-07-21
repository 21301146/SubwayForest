import Vue from 'vue'
import App from './App'
import router from './router'
import iView from 'iview';
import './assets/less/index.less';
import echarts from 'echarts'
import img from './lib/img'
import utils from "./lib/utils";
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

import BaiduMap from 'vue-baidu-map'



Vue.prototype.$echarts = function (el) {
    return echarts.init(el, null, {renderer: 'svg'})
}
Vue.prototype.$images = img
Vue.config.productionTip = false;
Vue.use(iView);
Vue.use(utils)
Vue.use(ElementUI)
Vue.use(BaiduMap, {
    // ak 是在百度地图开发者平台申请的密钥 详见 http://lbsyun.baidu.com/apiconsole/key */
    ak: 'TtFpXL5Q6O8EM6dsf0BvFM55GSHZDeKd'
})
new Vue({
  router,
  render: h => h(App)
}).$mount('#app')

