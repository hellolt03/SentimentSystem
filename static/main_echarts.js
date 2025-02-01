    <script>
        var chartDom = document.getElementById('mainOne');
        var myChart = echarts.init(chartDom);
        var option;
        var xData = {{ xData | tojson }};
        var yData = {{ yData | tojson }};
        var xRes = [];
        var yRes = [];
        for(var i=0;i<8;i++){
            xRes.push(xData[i])
            yRes.push(yData[i])
        }

        option = {
            tooltip: {// 自增
                trigger:"axis"
            },
            legend: {},// 自增
            toolbox: {// 自增
                show: true,
                feature: {
                  dataZoom: {
                    yAxisIndex: 'none'
                  },
                  dataView: { readOnly: false },
                  magicType: { type: ['line', 'bar'] },
                  restore: {},
                  saveAsImage: {}
                }
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            data: xRes
          },
          yAxis: {
            type: 'value'
          },
          series: [
            {
              name:"日期个数",
              data: yRes,
              type: 'line',
              areaStyle: {
                color:"rgba(0,128,255,0.2)"
              },
              smooth:true,
              lineStyle: {
                width:5
              },
              emphasis: {
                focus:"series"
              }
            }
          ]
        };

        let count = 8;
        setInterval(()=>{
            if(count >= xData.length) count=0
            xRes.shift()
            xRes.push(xData[count])
            yRes.shift()
            yRes.push(yData[count])
            count++
            myChart.setOption({
                xAxis: [{
                   data:xRes
                }],
                series: [{
                    data:yRes
                }]
            })
        },2000)

        option && myChart.setOption(option);

    </script>
    <script>
    var chartDom = document.getElementById('mainTwo');
    var myCharts = echarts.init(chartDom);
    var option;

    option = {
      title: {
        text: '各文章类型占比饼状图',
        left: 'center'
      },
      tooltip: {
        trigger: 'item'
      },
      legend: {
        orient: 'vertical',
        left: 'left',
          padding:[10,20,30,20],
          type: 'scroll',
      },
      series: [
        {
          name: '各文章类型占比饼状图',
          type: 'pie',
          radius: '50%',
          data: {{ typeChart | tojson }},
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

    option && myCharts.setOption(option);

    </script>
    <script>
        var chartDom = document.getElementById('mainThree');
        var myChart = echarts.init(chartDom);
        var option;

        option = {
          tooltip: {
            trigger: 'item'
          },
          legend: {
            top: '5%',
            left: 10,
              right:10,
              type: 'scroll',
          },
          series: [
            {
              name: '评论时间发布个数',
              type: 'pie',
              radius: ['60%', '50%'],
              avoidLabelOverlap: false,
              itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
              },
              label: {
                show: false,
                position: 'center'
              },
              emphasis: {
                label: {
                  show: true,
                  fontSize: 20,
                  fontWeight: 'bold'
                }
              },
              labelLine: {
                show: false
              },
              data: {{ createdAtChart | tojson }}
            }
          ]
        };

        option && myChart.setOption(option);

    </script>