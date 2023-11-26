/**图表 */
import { createRef, useEffect, useLayoutEffect, useMemo, useRef } from "react";
import * as echarts from 'echarts';
import { calHealthyText } from "@/pages/utils";

export interface Pie1DataProps{
    data: Array<{
    value: number,
    name: string,
}>}

export interface Pie2DataProps{
    data: Array<{
    value: number,
    name: string,
}>}

export interface Pie3DataProps{
  data: {
    arousal: number,
    pleasure: number
  }
}
export interface LineDataProps{
  data: {
    arousal: number[],
    pleasure: number[],
    timeInterval: string[],
  }
}

export interface RadarDataProps{
  data: Array<{
    name: string,
    value: number
  }>
}

export interface GaugueDataProps{
  data: number
}

export interface CircumplexProps{
  data: {
    activation: number,
    pleasant: number,
  }
}

export function Pie1Chart(props: Pie1DataProps){
    const {data} = props;
  
    useEffect(() => {
        const chartDom = document.getElementById('pie1');
        const myChart = echarts.init(chartDom);
        
        const option = {
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b}  {d}%"
            },
            legend: {
                top: '5%',
                left: 'center'
            },
            series: [
                {
                name: '情感比例',
                type: 'pie',
                radius: ['50%', '70%'],
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
                    fontSize: 40,
                    fontWeight: 'bold'
                    }
                },
                labelLine: {
                    show: false
                },
                data: data
            }
        ]
        };

        option && myChart.setOption(option);

    }, [data])
    
    
    
    return <div className="w-[20rem] h-[20rem]"  id='pie1'>
    </div>
}

export function Pie2Chart(props: Pie2DataProps){
    const {data} = props;
  
    useEffect(() => {
        const chartDom = document.getElementById('pie2');
        const myChart = echarts.init(chartDom);
        
        const option = {
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b}  {d}%"
            },
            legend: {
              top: 'top',
            },
            toolbox: {
              show: true,
              feature: {
                mark: { show: true },
              }
            },
            series: [
              {
                name: '情感分布',
                type: 'pie',
                radius: [20, 60],
                center: ['50%', '50%'],
                roseType: 'area',
                itemStyle: {
                  borderRadius: 8
                },
                data: data,
              }
            ]
          };

        option && myChart.setOption(option);

    }, [data])
    
    
    
    return <div className="w-[20rem] h-[20rem]"  id='pie2'>
    </div>
}


export function Pie3Chart(props: Pie3DataProps){
  const {data} = props;

  useEffect(() => {
      const chartDom = document.getElementById('pie3');
      const myChart = echarts.init(chartDom);
      
      const option = {
        tooltip: {
          trigger: 'item'
        },
        legend: {
          top: '10%',
          left: 'center',
        },
        series: [
          {
            name: 'Access From',
            type: 'pie',
            radius: ['40%', '60%'],
            center: ['50%', '60%'],
            // adjust the start angle
            startAngle: 180,
            label: {
              show: true,
              formatter(param: any) {
                // correct the percentage
                return param.name + ' (' + param.percent * 2 + '%)';
              }
            },
            data: [
              { value: data?.arousal, name: 'arousal' },
              { value: data?.pleasure, name: 'pleasure' },
            ]
          }
        ]
      }
      option && myChart.setOption(option);

  }, [data])
  
  
  
  return <div className="w-[20rem] h-[20rem]"  id='pie3'>
  </div>
}


export function LineChart(props: LineDataProps){

  const {data} = props;

  useEffect(() => {
      const chartDom = document.getElementById('line');
      const myChart = echarts.init(chartDom);
      const option = {
        title: {
          text: '心理走向',
          left: 'center', // Adjust the position as needed
        },
        legend: {
          data: ['Arousal', 'Pleasure'], // Legend labels corresponding to series names
          top: 'bottom', // Adjust the position as needed
        },
        xAxis: {
          type: 'category',
          data: data?.timeInterval.map(v=>v.split(' ')[1]) ?? []
        },
        yAxis: {
          type: 'value'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
          },
          formatter: function (params: any) {
            return params[0].name + '<br />' +
              params.map(function (item: any) {
                return item.seriesName + ': ' + item.value;
              }).join('<br />');
          },
        },      
        series: [
          {
            data: data?.arousal,
            type: 'line',
            name: 'Arousal',
            smooth: true,
            tooltip: {
              show: true,
            },
          },
          {
            data: data?.pleasure,
            type: 'line',
            name: 'Pleasure',
            smooth: true,
            tooltip: {
              show: true,
            },
          }
        ]
      };
      option && myChart.setOption(option);

  }, [data])
  
  
  
  return <div className="w-[36rem] h-[32rem] max-w-[50vw]"  id='line'></div>
}

export function RadarChart(props: RadarDataProps){
    const {data} = props;
    
    // const emotion_proportions = data.reduce((p, v) => {
    //     const newP = p;
    //     newP[v.name] = v.value
    //     return newP;
    // }, {
    //     sad: 0,
    //     angry: 0,
    //     surprise: 0,
    //     fear: 0,
    //     happy: 0,
    //     disgust: 0,
    //     neutral: 0,
    // } as {[name: string]: number});
    
    
    // // 快乐程度
    // const prousal = (0*emotion_proportions['surprise']+(-2)*emotion_proportions['fear']+(-3)*emotion_proportions['angry']+(-4)*emotion_proportions['disgust']+
    //        4*emotion_proportions['happy']+0*emotion_proportions['neutral']+(-4)*emotion_proportions['sad'])
    // // 活力程度
    // const arousal = (5*emotion_proportions['surprise']+3*emotion_proportions['fear']+2*emotion_proportions['angry']+1*emotion_proportions['disgust']+
    //        1*emotion_proportions['happy']+(-1)*emotion_proportions['neutral']+(-1)*emotion_proportions['sad'])
           
           
    const benchMark =  useMemo(() => [
        -20, 10, 0, 20, 0, 0, 20, 10, 20
    ], []);
    
    
    
    // const yoursData = useMemo(() => [
    //     0.71*prousal+0.12*arousal,
    //     -0.24*prousal,
    //     0.23*prousal+0.59*arousal,
    //     -0.26*prousal+0.37*arousal,
    //     0.48*arousal,
    //     0.37*prousal-0.44*arousal,
    //     0.35*prousal-0.20*arousal,
    //     -0.26*prousal+0.22*arousal,
    //     0.33*arousal,
    // ], [arousal, prousal])
    
    
    
    const obj = data?.map(v=> {
      return v.value
    }) ?? []
    
    const maxV = Math.max(...obj);
    
    useEffect(() => {
        const chartDom = document.getElementById('radar');
        const myChart = echarts.init(chartDom);
        
        const option = {
          color: ['#67F9D8', '#FFE434', '#56A3F1', '#FF917C'],
          title: {
            text: '心理分析'
          },
          legend: {
            top: 'bottom', // Adjust the position as needed
          },
          radar: [
            {
              indicator: [
                { text: '关怀', max: maxV },
                { text: '戒备', max: maxV },
                { text: '同理心', max: maxV },
                { text: '恐慌', max: maxV },
                { text: '自杀倾向', max: maxV },
                { text: '情绪稳定', max: maxV },
                { text: '社交期望', max: maxV },
                { text: '躁动', max: maxV },
                { text: '药物使用', max: maxV }
              ],
              radius: 120,
              axisName: {
                color: '#fff',
                backgroundColor: '#666',
                borderRadius: 3,
                padding: [3, 5]
              }
            }
          ],
          series: [
        
            {
              type: 'radar',
              radarIndex: 0,
              data: [
                {
                  value: benchMark,
                  name: 'benchMark',
                  symbol: 'rect',
                  symbolSize: 12,
                  lineStyle: {
                    type: 'dashed'
                  },
                  label: {
                    show: true,
                    formatter: function (params: any) {
                      return params.value;
                    }
                  }
                },
                {
                  value: obj ?? [],
                  name: '指数',
                  areaStyle: {
                    color: new echarts.graphic.RadialGradient(0.1, 0.6, 1, [
                      {
                        color: 'rgba(255, 145, 124, 0.1)',
                        offset: 0
                      },
                      {
                        color: 'rgba(255, 145, 124, 0.9)',
                        offset: 1
                      }
                    ])
                  }
                }
              ]
            }
          ]
        };

        option && myChart.setOption(option);

    }, [benchMark, maxV, obj])
    
    
    
    return <div className="w-[30rem] h-[30rem]  max-w-[60vw] my-[2rem]"  id='radar'>
    </div>
}


export function GaugeChart(props: GaugueDataProps){
  const {data} = props;

  useEffect(() => {
      const chartDom = document.getElementById('gaugue');
      const myChart = echarts.init(chartDom);
      
      const option = {
        series: [
          {
            type: 'gauge',
            startAngle: 180,
            endAngle: 0,
            center: ['50%', '75%'],
            radius: '90%',
            min: 0,
            max: 1,
            splitNumber: 8,
            axisLine: {
              lineStyle: {
                width: 6,
                color: [
                  [0.25, '#FF6E76'],
                  [0.5, '#FDDD60'],
                  [0.75, '#58D9F9'],
                  [1, '#7CFFB2']
                ]
              }
            },
            pointer: {
              icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
              length: '12%',
              width: 20,
              offsetCenter: [0, '-60%'],
              itemStyle: {
                color: 'auto'
              }
            },
            axisTick: {
              length: 12,
              lineStyle: {
                color: 'auto',
                width: 2
              }
            },
            splitLine: {
              length: 20,
              lineStyle: {
                color: 'auto',
                width: 5
              }
            },
            axisLabel: {
              color: '#464646',
              fontSize: 12,
              distance: -60,
              rotate: 'tangential',
              formatter: function (value: any) {
                if (value === 0.875) {
                  return '优秀';
                } else if (value === 0.625) {
                  return '良好';
                } else if (value === 0.375) {
                  return '中等';
                } else if (value === 0.125) {
                  return '异常';
                }
                return ''
              }
            },
            title: {
              offsetCenter: [0, '-10%'],
              fontSize: 12
            },
            detail: {
              fontSize: 30,
              offsetCenter: [0, '-35%'],
              valueAnimation: true,
              formatter: function (value: any) {
                return Math.round(value * 100) + '';
              },
              color: 'inherit'
            },
            data: [
              {
                value: data/100,
                name: '情绪健康度'
              }
            ]
          }
        ]
      }
      option && myChart.setOption(option);

  }, [data])
  
  
  
  return <div className="w-[30rem] h-[16rem] max-w-[60vw]"  id='gaugue'>
  </div>

}

export function CircumplexCanvas (props: CircumplexProps){
  
  const cRef = createRef<HTMLCanvasElement>();
  const trigger = useRef<boolean>(false);
  const {data} = props;

  
  useLayoutEffect(() => {
    if(cRef.current){
      const context = cRef.current.getContext('2d');
      // Example with an image URL
      const imageUrl = '/assets/Circumplex.png';
  
      const img = new Image();
      img.src = imageUrl;
  
      img.onload = function () {
        // Draw the image onto the canvas
        if(!trigger.current && context){
          context?.drawImage(img, 0, 50, img.width, img.height);
          context.beginPath();
          context.fillStyle = 'red';
          context.font = ' 20px red';
          const [x, y] = [(data.pleasant + 20)*(img.width / 40) / 1.42, (data.activation + 20)*(img.height / 40) / 1.20 + 10]
          context.arc(x, y, 5, 0, 2 * Math.PI);
          context.fillText('emotion state', x-10, y + 30)
         
          context.fill();
          context.closePath();
          trigger.current = true;
        }
      };
    }
    
  },[cRef, data.activation, data.pleasant])

  return <>
    <canvas ref={cRef} width={588} height={501} className="max-w-[60vw]"></canvas>
  </>
}