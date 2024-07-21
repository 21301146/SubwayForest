<template>
    <div class="doubleBarChart"></div>
</template>

<script>
import request from "@/utils/request";

export default {
    name: '',
    data() {
        return {
          topname : ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月'],
          topdata : [120, 102, 101, 134, 190, 130, 120, 190, 130, 120]
        }
    },
    methods: {
        async wbtopData(){
          var that = this;
          request.get("http://127.0.0.1:5000/subwaydealmoneytop10").then(res => {
            this.topdata.splice(0);
            this.topname.splice(0);
            for(let i = 0;i < res.data.length;i++)
            {
              that.topname.push(res.data[i]['name']);
              that.topdata.push(res.data[i]['value']);
            }
            that.setChart();
          })

        },
        formatYAxisValue(value) {
          if (value >= 100000) {
            return (value / 1000000).toLocaleString() + 'KK'
          } else {
            return value.toString()
          }
        },

        setChart() {
            let option = {
                // tooltip是提示框
                tooltip: {
                    // 触发类型为坐标轴触发
                    trigger: 'axis',
                    axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                        type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                    },
                    backgroundColor: '#11367a',
                    textStyle: {
                        color: '#ffffff',
                        fontSize: 15,
                    },
                },
                // 对图形组件的相关配置
                legend: [
                    {
                        top: '8%',
                        right: '5%',
                        itemWidth: 7,
                        itemHeight: 7,
                        textStyle: {
                            color: '#5CB1C1',
                        }
                    },
                ],
                // 调整容易的上下左右的位置
                grid:
                    {
                        top: '15%',
                        left: '3%',
                        right: '5%',
                        bottom: '8%',
                        containLabel: true,
                    },
                // x轴配置
                xAxis: [
                    {
                        type: 'value',
                        splitNumber: 5,
                        max: 6500000,
                        min: 0,
                        interval: 500000,
                        axisLabel: {
                            interval: 0,
                            color: '#61B9C8',
                            fontSize: 10,
                            formatter: this.formatYAxisValue
                        },
                        axisLine: {
                            symbol: ['none', 'arrow'],
                            symbolSize: [6, 6],
                            symbolOffset: [0, 5],
                            lineStyle: {
                                color: '#122C49'
                            }
                        },
                        axisTick: {show: false},
                        boundaryGap: [0.5, 0.5]
                    },
                ],
                // y轴配置
                yAxis:
                    {
                        type: 'category',
                        min: 0,
                        // 这里max是调整y轴数据显示的个数
                        max: 10,
                        splitNumber: 5,
                        boundaryGap: [0.9, 0.5],
                        barGap: 36,
                        axisLabel: {
                            color: '#61B9C8',
                            fontSize: 9,
                            showMaxLabel: false,
                        },
                        axisLine: {
                            symbol: ['none', 'arrow'],
                            symbolSize: [6, 6],
                            symbolOffset: [0, 5],
                            lineStyle: {
                                color: '#ffffff'
                            }
                        },
                        axisTick: {
                            length: 3
                        },
                        name: '(地区名称)',
                        nameGap: 30,
                        nameTextStyle: {
                            color: '#61B9C8',
                            fontSize: 10,
                            align: 'right',
                            padding: [0, 6, 0, 0]
                        },
                        splitLine: {show: false},
                        data: this.topname
                    },
                series: [
                    {
                        name: '营业额',
                        type: 'bar',
                        barWidth: 7,
                        stack: '总数',
                        barGap: 120,
                        label: {
                          show: true,
                          position: 'top',
                          formatter: '{c}',  // 数值显示格式
                          textStyle: {
                            color: '#ffffff'  // 设置文字颜色为红色
                          }
                        },
                        itemStyle: {
                            color: {
                                type: 'linear',
                                x: 5,
                                y: 10,
                                x2: 0,
                                y2: 1,
                                colorStops: [{
                                    offset: 0, color: '#FC9386' // 0% 处的颜色
                                },
                                    {
                                        offset: 0.4, color: '#F87B86' // 40% 处的颜色
                                    }, {
                                        offset: 1, color: '#F36087' // 100% 处的颜色
                                    }],
                                global: false // 缺省为 false
                            }, //背景渐变色
                            barBorderRadius: [3.5, 3.5, 0, 0],
                        },
                        data: this.topdata
                    },

                ]
            };
            let myChart = this.$echarts(this.$el);
            myChart.clear();
            myChart.resize()
            myChart.setOption(option);
        }
    },
    mounted() {
        this.wbtopData();
        this.setChart()
    },
    created(){
      this.wbtopData();
      this.setChart()
    }
}
</script>

<style lang="less" scoped>
.doubleBarChart {
    width: 100%;
    height: 100%;
}
</style>
