/* eslint-disable @next/next/no-img-element */
import Bar from "@/components/Bar";
import getStream from "@/utils/camera";
import { getEmotion } from "@/utils/socket/getEmotion";
import { Slider } from "@mui/material";
import { useRouter } from "next/router"
import { useCallback, useEffect, useRef, useState } from "react"
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import { throttle } from "lodash";
import { Pie1Chart, Pie1DataProps, Pie2Chart, RadarChart } from "@/components/Chart";
import { updatePie1Data } from "@/utils/method/updatePie1Data";
import CircularProgress from '@mui/material/CircularProgress';

export default function Report() {

  const router = useRouter();
  
  const {id} = router.query;
  
  const imgRef = useRef<HTMLImageElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const emotion = useRef<string>('');
  const clickRef = useRef<number>(0);
  const faceBox = useRef<number[][]>([[0, 0, 0, 0]]);
  const timer = useRef<number>(0);
  const workConfig = useRef({
    fre: 0.5,
    time: 10,
  })
  const state = useRef<'pause' | 'pending' | 'cal' | 'finish'>('pause');
  const [imgSrc, setImgSrc] =  useState('');
  const [expressState, setExP] = useState<'pause' | 'pending' | 'cal' | 'finish'>('pause');
  

  //当前采集到的数据
  const [curPie1Data, setcurPie1Data] = useState<Pie1DataProps['data']>([]);
  //采集三种状态
  
  //向后端获取情绪数据 根据当前获取频率进行
  const gEmotion = useCallback(async () => {
    if(state.current === 'pending' && (timer.current - clickRef.current == workConfig.current.fre || timer.current == 0) ){
      timer.current = clickRef.current;
      const emotions = (await getEmotion()).data;
      emotion.current = emotions.data;
      faceBox.current = emotions.face_data;
      setcurPie1Data( v  => updatePie1Data(v, emotions.data)); 
    }
  }, []);
  
  const startToGetData = () => {
    //总共采集帧数
    clickRef.current = workConfig.current.time;
    const interval = setInterval(() => {
      if(clickRef.current === 0){
        // state.current = 'cal';
        setExP('cal');
        clearInterval(interval);
      }else{
        if(workConfig.current.fre === 0.5){
          gEmotion()
        }else if(clickRef.current % workConfig.current.fre === 0){
          gEmotion()
        }
        clickRef.current-=0.5;
      }
      //0.5秒的精度查询当前的时间倒计时
    }, 500);
  }
  
  const draw = (ctx:  CanvasRenderingContext2D) => {
    const loop = () => {
      if(imgRef.current && state.current !== 'finish') {
        const {width, height} = imgRef.current;
        const radius = width / height;
        ctx?.drawImage(imgRef.current, -480 * radius / 4, 0, 480 * radius, 480);
        ctx.strokeStyle = '#3266e9'; //邊框顏色
        ctx.font = "32px Microsoft YaHei";
        faceBox.current.map((facePos, idx) => {
          if(state.current !== 'finish' && state.current !== 'cal'){
            //等比例缩小到高度为480的拍摄
            const strokeRadius = 480 / height
            ctx.strokeRect(facePos[0] * strokeRadius -480 * radius / 4, facePos[1]  * strokeRadius, facePos[2] * strokeRadius, facePos[3] * strokeRadius);  //只有框線的矩形
            ctx.fillText(emotion.current[idx], facePos[0] * strokeRadius - 480 * radius / 4 , facePos[1] * strokeRadius - 10);
          }
          
        })
      }
      requestAnimationFrame(loop);
    }    
    requestAnimationFrame(loop);
  }
  
  const init = async () => {
      if(imgRef.current){
        const ctx = canvasRef.current?.getContext('2d');
        if(ctx) draw(ctx);
      }
  }
  
  useEffect(() => {
    state.current = expressState;
  }, [expressState])
  
  useEffect(() => {
    if(expressState === 'cal'){
      setTimeout(() => {
        setExP('finish');
      }, 1000);
    }
  }, [expressState])

  useEffect(() => {
    init()
    requestIdleCallback(() => {
      setImgSrc(`http://${location.hostname}:8080/video_feed`);
    })
    
  }, [])
  
  

  return (
    <main
      className='w-screen h-screen flex flex-col '
    >
      <Bar bgColor={'primary'}></Bar>
      <div className="flex flex-row w-full h-full mt-20"
        style={{flexDirection: expressState === 'finish' ? 'column' : 'row'}}>
        <div 
          className="left-pan mt-10 ml-20 flex flex-col relative items-center justify-center"
          style={expressState === 'finish' ? {margin: 0}: {} }>
            { 
              expressState!=='finish' && <div className="absolute top-[6rem] left-4 flex justify-center items-center">
                  <div className="w-3 h-3 rounded-full" style={{background: 'red'}}></div>
                  <div className="mx-2" style={{color: 'red'}}>REC</div> 
              </div> 
            }
            <canvas className="rounded-2xl bg-black transition-all" 
              height={480} 
              width={480} 
              style={{transform: expressState==='finish' ? 'scale(0.5)': ''}}
              ref={canvasRef}>
            </canvas>
            {/* <Pie2Chart data={curPie1Data}/> */}

            <img src={imgSrc} ref={imgRef} alt="img" hidden></img>
            {/* <video autoPlay playsInline ref={imgRef} preload="auto"></video> */}
        </div>
        
        <div className="right-pan flex flex-col flex-1 text-black items-center">
            {/* 表单控件 工作于pause阶段*/}
            { expressState === 'pause' && <div className="form w-1/2 mt-36 transition-all relative">
                <h1 className="text-3xl my-6">视频采集设置</h1>
                <p>采集秒数</p>
                <p className="text-xs opacity-20"> 总共采集的时长</p>
                <Slider
                    aria-label="Temperature"
                    defaultValue={10}
                    getAriaValueText={(v) => `${v}s`}
                    valueLabelDisplay="auto"
                    step={10}
                    marks
                    min={10}
                    max={120}
                    onChange={(e) => {
                        workConfig.current = {
                          ...workConfig.current,
                          time: (e?.target as {value: number} | null)?.value ?? 0
                        }
                    }}
                />

                <p>采集精细度</p>
                <p className="text-xs opacity-20">  每秒采集帧数</p>
                <Slider
                    aria-label="Temperature"
                    defaultValue={0.5}
                    getAriaValueText={(v) => `${v}s`}
                    valueLabelDisplay="auto"
                    step={0.5}
                    marks
                    min={0.5}
                    max={2}
                    onChange={(e) => {
                      workConfig.current = {
                        ...workConfig.current,
                        fre: (e?.target as {value: number} | null)?.value ?? 0
                      }
                    }}
                />
                <button 
                    className="bg-primary w-16 h-16 rounded-full font-white hover:opacity-70 transition-all mt-10"
                    onClick={() => {
                        setExP('pending');
                        startToGetData();
                    }}>
                    <NavigateNextIcon 
                        className="text-white w-8 h-8"
                    />
                </button>
                
            </div> }
            
            {/* 展示控件 工作于pending阶段*/}
            { expressState  === 'pending' && <div className="form w-1/2 mt-36 transition-all relative">
              <h1 className="text-3xl my-6">正在采集中</h1>
              <div className="text-4xl text-primary"> {Math.round(clickRef.current)} s</div>
            </div> }
            
            {/* 计算控件 工作于cal阶段 */}
            { expressState  === 'cal' && <div className="form w-1/2 mt-36 transition-all relative">
              <h1 className="text-3xl my-6">正在生成报告中</h1>
              <CircularProgress />
            </div> }
            
            {/* 报告控件 工作于finish阶段 */}
            { expressState  === 'finish' && <div className="form w-4/5 transition-all relative h-[100vh]">
              <h1 className="text-3xl my-6 text-center">您的情绪得分为</h1>
              
              <div className="text-4xl text-[#20a60d] text-center"> 98 </div>
              {/* 绘图面板 */}
              <div className="mt-20 flex flex-wrap justify-between">
                <div className="flex justify-center flex-col items-center">
                  <span className="text-xl">情绪比例</span>
                  <Pie1Chart data={curPie1Data}/>
                </div>
                <div className="flex justify-center flex-col items-center">
                  <span className="text-xl">情感分布</span>
                  <Pie2Chart data={curPie1Data}/>
                </div>
                
                <div className="flex justify-center flex-col items-center">
                  <span className="text-xl">心理分析</span>
                  <RadarChart data={curPie1Data}/>
                </div>
                
              </div>
              
            </div> }
            
        </div>
        
      </div>
      
    
    </main>
  )
}
