<template>
    <div class="page2">
      <el-button type="primary" style="position: absolute;top: 15px;right: 40px" onclick="window.location.href = 'http://localhost:9876/'">退出登录</el-button>
        <Row class='content'>
            <Col span="8">
                <div class="list" style="height:350px">
                    <div class="left">
                        <span class='title'><span class="title-4">各线路营业额占比</span></span>
                        <span class="angle1"></span>
                        <span class="angle2"></span>
                        <span class="angle3"></span>
                        <span class="angle4"></span>
                        <div class="chart-68">
                            <area-chart ref="chart1" id="left_1" :select-range-date="selectRangeDate" :config="cnfigData1" style="padding-left: 15%"></area-chart>
                        </div>
                    </div>
                </div>
                <div class="list" style="height: 350px">
                    <div class="left">
                        <span class='title'><span class="title-8">各站进出累计人数</span></span>
                        <span class="angle1"></span>
                        <span class="angle2"></span>
                        <span class="angle3"></span>
                        <span class="angle4"></span>
                        <div class="chart-68">
                            <bar-chart ref="chart3" id="left_3" :config="configData2" style="padding-left: 15%"></bar-chart>
                        </div>
                    </div>
                </div>

            </Col>
            <Col span="8">
              <div class="chart-68">
                <baidu-map class="map" center="深圳" style="padding-top: 10%">
                 <bm-marker v-for="location in locations" :key="location.id" :position="location.position" @click="infoWindowOpen(location.id)">
                 </bm-marker>
                 <bm-info-window :position="position" :show="show" @close="infoWindowClose" @open="infoWindowOpen">
                  <p>{{ title }}</p>
                    <p>{{ content1 }}</p>
                  <p>{{ content2 }}</p>
                    <p>{{ content3 }}</p>
                 </bm-info-window>
                  <bm-navigation anchor="BMAP_ANCHOR_TOP_RIGHT"></bm-navigation>
                </baidu-map>
              </div>
            </Col>
            <Col span="8">
                <div class="list" style="height: 700px">
                    <div class="right">
                        <span class='title'><span class="title-4">各站营业额top10</span></span>
                        <span class="angle1"></span>
                        <span class="angle2"></span>
                        <span class="angle3"></span>
                        <span class="angle4"></span>
                        <div class="chart-32">
                        </div>
                        <div class="chart-68">
                            <double-bar-chart ref="chart6"></double-bar-chart>
                        </div>
                    </div>
                </div>

            </Col>
        </Row>
    </div>
</template>

<script>
import request from "@/utils/request";

const areaChart = ()=> import('./components/areaChart');
const barChart = () => import('./components/page2/barChart');
const doubleBarChart = ()=> import('./components/page2/doubleBarChart');

// const baidumap  = () => import('./components/page2/baidumap');


export default {
    name: 'page2',
    props: ['selectRangeDate'],
    components: {
        areaChart,
        barChart,
        doubleBarChart,
        // baidumap
    },
    data() {
        return {

            position: { lng: 113.930372, lat: 22.517096 }, // 指定地点的经纬度】
            title : "长隆",
            content1 : "测试1",
            content2 : "测试2",
            content3 : "测试3",
            show: false,


            locations: [
              {
                id: 1,
                position: { lng: 113.930372, lat: 22.517096 },
                'content1' : "测试1",
                'content2' : "测试2",
                'content3' : "测试3",
              },
              {
                id: 2,
                position: { lng: 113.932050, lat: 22.520518 },
                'content1' : "测试1",
                'content2' : "测试2",
                'content3' : "测试3",
              },
            ],

            nowRanges : 59,
            everyPer: 0,
            xOffset: 0,
            circle: {
                x: 250,
                y: 250,
                radius: 218
            },
            cnfigData1: {
                color: '#5CB1C1',
                name: ['（指标量）'],
                data: [
                    {
                        name: '二手交易额',
                        color: ['#9e70ff', '#6e5eff'],
                        data: [200, 12, 21, 54, 260, 130, 210],
                    }
                ]
            },
            configData2: {
                data: [213, 12, 137, 99, 63, 196, 248, 212, 248, 112]
            },



            warea: {x: 250, y: 250, max: 700},
            dots: [],
            resizeFn: null,
            animationFrame1:null,
            animationFrame2: null,
            centerBox: {
                width: 0,
                height: 0
            }
        }
    },
    methods: {

        infoWindowClose () {
          this.show = false
        },
        infoWindowOpen (id) {
          for(let i = 0; i < this.locations.length;i++){
            if(this.locations[i]['id'] == id){
              this.title = this.locations[i]['title']
              this.content1 = this.locations[i]['content1']
              this.content2 = this.locations[i]['content2']
              this.content3 = this.locations[i]['content3']
              this.position = this.locations[i]['position']
              break
            }
          }
          this.show = true;

        },

        wbUser(){
          request.get("http://127.0.0.1:5000/subwaymapinfo").then(res => {
            console.log(res.data);
            this.locations = res.data;
          })
        },


    },
    mounted() {
       this.wbUser();

    },
  beforeDestroy() {
        window.removeEventListener('resize', this.resizeFn)
        window.cancelAnimationFrame(this.animationFrame1)
        window.cancelAnimationFrame(this.animationFrame2)
    }
}
</script>

<style lang="less" scoped>
.page2 {
    height: 100%;
    width: 100%;
    padding: 14px 20px 20px;
    background: #03044A;
    overflow: hidden;

    .content {
        height: 65%;

        .ivu-col {
            height: 100%;
        }

        .circlePie {
            height: 100%;
            padding: 0 0 40px;
            text-align: center;
            position: relative;

            canvas {
                position: absolute;
                left: 50%;
                top: 0;
                transform: translate(-50%, 0);
            }

            #dot {
                background: rgba(0, 0, 0, 0);
            }
        }

        .list {
            height: 48%;

            .left, .right {
                background: #0D1341;
            }

            .left, .right, .center {
                width: 100%;
                height: 90%;
                border: 1px solid #0D2451;
                position: relative;

                #left1, #left2, #left3, #right1, #right2, #right3, #center2 {
                    height: 100%;
                }

                .chart-68 {
                    width: 75%;
                    height: 100%;
                    float: left;
                }

                .chart-32 {
                    width: 15%;
                    height: 100%;
                    float: left;
                }
            }
        }
    }

    .bottom-list {
        height: 35%;

        .ivu-col {
            height: 100%;

            .list {
                height: 100%;
                width: 33.3333%;
                padding-right: 1.5%;
                float: left;

                #bottom_4 {
                    padding: 0 20px;
                }

                .bottom {
                    width: 100%;
                    height: 100%;
                    border: 1px solid #0D2451;
                    position: relative;
                }
            }

            .right-bottom {
                width: 100%;
                padding-right: 0;

                .bottom1 {
                    width: 100%;
                }
            }
        }
    }

}

.bm-view {
  width: 100%;
  height: 300px;
}

.map {
  width: 100%;
  height: 400px;
}

.map[data-v-0e2a1c59]{
  height: 600px !important;
}
</style>
