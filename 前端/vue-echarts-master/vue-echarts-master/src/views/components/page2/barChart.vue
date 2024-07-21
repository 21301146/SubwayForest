<template>
    <div class="barChart"></div>
</template>

<script>
import request from "@/utils/request";

export default {
    name: '',
    data() {
        return {
          datavalue1 : [55, 190, 137, 99, 63, 196, 248, 212, 248, 112],
          datavalue2 : [55, 190, 137, 99, 63, 196, 248, 212, 248, 112],
          dataname: ["布吉", "长龙", "双龙", "红岭南", "后亭", "等良", "梅静", "赤尾", "深惠3B线", "银湖"]
        }
    },
    methods: {

        formatYAxisValue(value) {
          if (value >= 100000) {
            return (value / 1000000).toLocaleString() + 'KK'
          } else {
            return value.toString()
          }
        },

        bwks(){
          request.get("http://127.0.0.1:5000/subwayinfomation").then(res => {
            this.dataname.splice(0);
            this.datavalue1.splice(0);
            this.datavalue2.splice(0);
            for(let i = 0;i < res.data.length;i++)
            {
              this.dataname.push(res.data[i]['name']);
              this.datavalue2.push(res.data[i]['value1']);
              this.datavalue1.push(res.data[i]['value2']);
            }
            this.setChart()
          })
        },

        setChart() {
            let option = {
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                        type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                    },
                    backgroundColor: '#11367a',
                    textStyle: {
                        color: '#6dd0e3',
                        fontSize: 10,
                    },
                },
                legend: {
                    left: "11%",
                    top: "15%",
                    itemWidth: 7,
                    itemHeight: 7,
                    textStyle: {
                        color: '#5CB1C1',
                    }
                },
                grid: {
                    top: '12%',
                    bottom: '12%',
                    left: "10%",
                    right: '10%',
                    containLabel: false
                },
                xAxis: [
                    {
                        type: 'category',
                        boundaryGap: true,
                        axisLine: {
                            symbol: ['none', 'arrow'],
                            symbolSize: [6, 6],
                            symbolOffset: [0, 10],
                            lineStyle: {
                                color: '#122C49'
                            }
                        },
                        axisTick: {show: false},
                        axisLabel: {
                            color: '#61B9C8',
                            fontSize: 10,
                            interval: 0,
                        },
                        data: this.dataname
                    }
                ],
                yAxis: [
                    {
                        type: 'value',
                        scale: true,
                        max: 10000000,
                        min: 0,
                        interval: 500000,
                        axisLine: {
                            symbol: ['none', 'arrow'],
                            symbolSize: [6, 6],
                            lineStyle: {
                                color: '#122C49'
                            }
                        },
                        axisLabel: {
                            color: '#61B9C8',
                            showMaxLabel: false,
                            fontSize: 10,
                            formatter: this.formatYAxisValue
                        },
                        splitLine: {
                            show: false,
                        },
                        name: '(指标量)',
                        nameGap: -5,
                        nameTextStyle: {
                            color: '#61B9C8',
                            fontSize: 9,
                            align: 'right',
                            padding: [0, 4, 0, 0]
                        },
                    }
                ],
                series: [
                    {
                        name: '进口人数',
                        type: 'bar',
                        itemStyle: {
                            color: "#50A2F6"
                        },
                        barWidth: 10,
                        barCategoryGap: 10,
                        data: this.datavalue1
                    },
                    {
                      name: '出口人数',
                      type: 'bar',
                      itemStyle: {
                        color: "#DF7DFD"
                      },
                      barWidth: 10,
                      barCategoryGap: 10,
                      data: this.datavalue2
                    }
                ]
            };
            let myChart = this.$echarts(this.$el);

            myChart.clear();
            myChart.resize()
                myChart.setOption(option);
        }
    },
    mounted() {
        this.bwks();
        this.setChart()
    },
}
</script>

<style lang="less" scoped>
.barChart {
    width: 100%;
    height: 100%;
}
</style>
