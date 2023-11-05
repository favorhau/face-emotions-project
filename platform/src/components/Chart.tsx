/**图表 */
import { useEffect, useMemo } from "react";
import * as echarts from 'echarts';

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
    const transfer: {
        [name: string]: string[]
    } = { 
        'active': ['surprise', 'fear', 'angry', 'disgust', 'happy'],
        'neutral': ['neutral'],
        'inacitive': ['sad'],
    }
    
   
    const inTransfer = Object.keys(transfer).reduce((p, c) => {
        const value = transfer[c];
        return [...p,
        {
            name: c,
            value: data.reduce((dp, dc) => {
                if (value.includes(dc.name)) {
                    return dp + dc.value;
                } else {
                    return dp;
                }
            }, 0)
        }
        ];
    }, [{}]) as unknown as Pie2DataProps['data']
  
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
                data: inTransfer,
              }
            ]
          };

        option && myChart.setOption(option);

    }, [inTransfer])
    
    
    
    return <div className="w-[20rem] h-[20rem]"  id='pie2'>
    </div>
}


export function RadarChart(props: Pie2DataProps){
    const {data} = props;
    
    const emotion_proportions = data.reduce((p, v) => {
        const newP = p;
        newP[v.name] = v.value
        return newP;
    }, {
        sad: 0,
        angry: 0,
        surprise: 0,
        fear: 0,
        happy: 0,
        disgust: 0,
        neutral: 0,
    } as {[name: string]: number});
    
    
    // 快乐程度
    const prousal = (0*emotion_proportions['surprise']+(-2)*emotion_proportions['fear']+(-3)*emotion_proportions['angry']+(-4)*emotion_proportions['disgust']+
           4*emotion_proportions['happy']+0*emotion_proportions['neutral']+(-4)*emotion_proportions['sad'])
    // 活力程度
    const arousal = (5*emotion_proportions['surprise']+3*emotion_proportions['fear']+2*emotion_proportions['angry']+1*emotion_proportions['disgust']+
           1*emotion_proportions['happy']+(-1)*emotion_proportions['neutral']+(-1)*emotion_proportions['sad'])
           
           
    const benchMark =  useMemo(() => [
        -20, 10, 0, 20, 0, 0, 20, 10, 20
    ], []);
    
    
    
    const yoursData = useMemo(() => [
        0.71*prousal+0.12*arousal,
        -0.24*prousal,
        0.23*prousal+0.59*arousal,
        -0.26*prousal+0.37*arousal,
        0.48*arousal,
        0.37*prousal-0.44*arousal,
        0.35*prousal-0.20*arousal,
        -0.26*prousal+0.22*arousal,
        0.33*arousal,
    ], [arousal, prousal])
    
  
    useEffect(() => {
        const chartDom = document.getElementById('radar');
        const myChart = echarts.init(chartDom);
        
        const option = {
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b} "
            },
            legend: {
              data: ['benchmark', 'yours']
            },
            radar: {
              // shape: 'circle',
              indicator: [
                { name: '关怀', max: 20 },
                { name: '戒备', max: 30 },
                { name: '同理心', max: 40 },
                { name: '恐慌', max: 50 },
                { name: '自杀倾向', max: 50 },
                { name: '情绪稳定', max: 80 },
                { name: '社交期望', max: 40 },
                { name: '躁动', max: 40 },
                { name: '药物使用', max: 60 },
                
              ]
            },
            series: [
              {
                name: '心理分析',
                type: 'radar',
                data: [
                  {
                    value: benchMark,
                    name: 'benchmark'
                  },
                  {
                    value: yoursData,
                    name: 'yours'
                  }
                ]
              }
            ]
        };

        option && myChart.setOption(option);

    }, [benchMark, yoursData])
    
    
    
    return <div className="w-[20rem] h-[20rem]"  id='radar'>
    </div>
}