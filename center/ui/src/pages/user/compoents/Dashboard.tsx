import { Typography, CircularProgress, Box } from '@mui/material';
import React, { useEffect, useState } from 'react';
import logo from '../../../../public/assets/device.jpg'
import Image from 'next/image';
import * as echarts from 'echarts';

export default function Dashboard(){
    
    useEffect(() => {
        
        
        const chartDom = document.getElementById('emotion_trend');
        const myChart = echarts.init(chartDom);
        
        const option = {
        title: {
            text: 'Trends of Emotion',
            subtext: 'Multidimensional Emotion Analysis'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
            type: 'cross'
            }
        },
        toolbox: {
            show: true,
            feature: {
            saveAsImage: {}
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            // prettier-ignore
            data: ['00:00', '01:15', '02:30', '03:45', '05:00', '06:15', '07:30', '08:45', '10:00', '11:15', '12:30', '13:45', '15:00', '16:15', '17:30', '18:45', '20:00', '21:15', '22:30', '23:45']
        },
        yAxis: {
            type: 'value',
            axisLabel: {
            formatter: '{value} W'
            },
            axisPointer: {
            snap: true
            }
        },
        visualMap: {
            show: false,
            dimension: 0,
            pieces: [
            {
                lte: 6,
                color: 'green'
            },
            {
                gt: 6,
                lte: 8,
                color: 'red'
            },
            {
                gt: 8,
                lte: 14,
                color: 'green'
            },
            {
                gt: 14,
                lte: 17,
                color: 'red'
            },
            {
                gt: 17,
                color: 'green'
            }
            ]
        },
        series: [
            {
            name: 'Electricity',
            type: 'line',
            smooth: true,
            // prettier-ignore
            data: [300, 280, 250, 260, 270, 300, 550, 500, 400, 390, 380, 390, 400, 500, 600, 750, 800, 700, 600, 400],
            markArea: {
                itemStyle: {
                color: 'rgba(255, 173, 177, 0.4)'
                },
                data: [
                [
                    {
                    name: '早上',
                    xAxis: '07:30'
                    },
                    {
                    xAxis: '10:00'
                    }
                ],
                [
                    {
                    name: '下午',
                    xAxis: '17:30'
                    },
                    {
                    xAxis: '21:15'
                    }
                ]
                ]
            }
            }
        ]
        };

        myChart.setOption(option);
        
    }, [])
    return <div className='w-full h-full flex flex-wrap text-black justify-start'>
        <div className='w-full min-w-[18rem] max-w-[28rem] h-[15rem] bg-white rounded-xl shadow-md mx-[1rem] mt-[2rem] p-[1rem] relative'>
            <Typography variant='h6'>设备情况</Typography>
            <Typography variant='h3' className='text-success pl-2 relative' style={{zIndex:88}} >1 <text className='text-sm'>在线</text></Typography>
            
            <Typography variant='h5' className='text-error pl-4 relative' style={{zIndex:88}}>0 <text className='text-xs'>离线</text></Typography>
            <Typography variant='overline' className='text-invaild pl-2  absolute left-6 bottom-6' style={{zIndex:88}}>1秒前 曾上传数据</Typography>
            <Image className='absolute right-1 bottom-3'style={{zIndex: 0}} src={logo} width={250} height={250} alt='device'></Image>
        </div>
        
        <div className='w-full min-w-[18rem] max-w-[50rem] min-h-[15rem] bg-white rounded-xl shadow-md mx-[1rem] mt-[2rem] p-[1rem] relative'>
            <Typography variant='h6'>总体用户状态</Typography>
            <div className='flex flex-row flex-wrap'>
                <div className='flex mt-[2rem] h-[8rem] w-[10rem] flex-col justify-around items-center'>
                    <Box sx={{ position: 'relative', display: 'inline-flex' }}>
                        <CircularProgress variant="determinate" value={90} size={90} color='success'/>
                        <Box
                            sx={{
                            top: 0,
                            left: 0,
                            bottom: 0,
                            right: 0,
                            position: 'absolute',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            }}
                        >
                            <Typography
                            variant="caption"
                            component="div"
                            color="text.secondary"
                            >{`98%`}</Typography>
                        </Box>
                    </Box>
                    <Typography className='text-invaild' variant='subtitle2'>健康度</Typography>
                </div>
                
                <div className='flex mt-[2rem] h-[8rem] w-[10rem] flex-col justify-around items-center'>
                    <Typography variant='h3' className='text-black relative' style={{zIndex:88}}>1028</Typography>
                    <Typography className='text-invaild' variant='subtitle2'>数据条数</Typography>
                </div>
                <div className='flex mt-[2rem] h-[8rem] w-[10rem] flex-col justify-around items-center'>
                    <Typography variant='h3' className='text-error relative' style={{zIndex:88}}>8</Typography>
                    <Typography className='text-invaild' variant='subtitle2'>异常用户</Typography>
                </div>
            </div>
        </div>
        <div className='w-full min-w-[20rem] max-w-[80rem] h-[35rem] bg-white rounded-xl shadow-md mx-[1rem] mt-[2rem] p-[1rem] relative'>
            <Typography variant='h6'>情绪趋势</Typography> 
            <div id="emotion_trend" className='min-w-[20rem] max-w-[80rem] h-[30rem]'> </div>
        </div>
        
    </div>
}