<template>
    <div class="area" id="areas"></div>
</template>

<script>

// eslint-disable-next-line no-unused-vars
import echarts from 'echarts'
import request from "@/utils/request";
export default {
    name: "areaChart",
    props: [ 'config', 'selectRangeDate'],
    data() {
        return {
          datas: [
            { value: 1048, name: '地铁5号线' },
            { value: 735, name: '地铁2号线' },
            { value: 580, name: '地铁1号线' },
            { value: 484, name: '地铁6号线' },
            { value: 300, name: '新华南车' }
          ],
        }
    },
    methods: {

        dtzb(){
          request.get("http://127.0.0.1:5000/Turnoverforaccounted").then(res => {
            this.datas = res.data;
            this.setChart()
          })
        },

        setChart() {
          let option = {
            tooltip: {
              trigger: 'item'
            },
            series: [
              {
                name: 'Access From',
                type: 'pie',
                radius: '50%',
                data: this.datas,
                emphasis: {
                  itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                  }
                }
              }
            ]
          };


            let myChart = this.$echarts(this.$el);
            myChart.setOption(option);
        }
    },
    mounted() {
        this.dtzb();
        this.setChart();
    }
}
</script>

<style lang="less" scoped>
.area {
    height: 100%;
}
</style>
