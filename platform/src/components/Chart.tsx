/**图表 */
import { useEffect } from "react";
import * as echarts from 'echarts';

export interface Pie1DataProps{
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
    
    
    
    return <div className="w-[18rem] h-[18rem]" id='pie1'>
    </div>
}

export function Pie2Chart(props: Pie1DataProps){
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
    
    
    
    return <div className="w-[18rem] h-[18rem]" id='pie1'>
    </div>
}