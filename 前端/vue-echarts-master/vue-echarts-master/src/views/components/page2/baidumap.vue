<template>
  <baidu-map class="bm-view">
  </baidu-map>
</template>


<script>
import BaiduMap from 'vue-baidu-map/components/map/Map.vue'
export default {
  components: {
    BaiduMap
  },
  data(){
    return {
      position: { lng: 113.930372, lat: 22.517096 }, // 指定地点的经纬度
      title: '指定地点标题', // 指定地点的标题
      content: '指定地点信息' // 指定地点的详细信息
    }
  }
}
</script>

<style>
.bm-view {
  width: 100%;
  height: 300px;
}
</style>
