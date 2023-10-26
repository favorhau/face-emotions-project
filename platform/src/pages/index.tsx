import getStream from "@/utils/camera";
import { getEmotion } from "@/utils/socket/getEmotion";
import { useEffect, useRef, useState } from "react"
import {throttle} from 'lodash';

export default function Home() {

  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [canvasBox, setCanvasBox] = useState({
    width: 0,
    height: 0,
  })
  const emotion = useRef<string>('');
  const faceBox = useRef<number[][]>([[0, 0, 0, 0]]);
  
  
  const gE = throttle(async (imgData: string) => {
   const emotions = (await getEmotion(imgData)).data;
   emotion.current = emotions.data;
   faceBox.current = emotions.face_data;
  }, 500)
  
  const draw = (ctx:  CanvasRenderingContext2D) => {
    const loop = () => {
      if(videoRef.current) {
        ctx?.drawImage(videoRef.current, 0, 0);
        ctx.strokeStyle = '#0000ff'; //邊框顏色
        ctx.font = "32px Microsoft YaHei";
        faceBox.current.map(facePos => {
          ctx.strokeRect(facePos[0], facePos[1] ,facePos[2], facePos[3]);  //只有框線的矩形
          ctx.fillText(emotion.current, facePos[0], facePos[1])
        })
        // ctx.
      }
      const imgData = canvasRef.current?.toDataURL('image/jpeg', 0.2) ?? '';
      
      gE(imgData);
      requestAnimationFrame(loop);
    }    
    requestAnimationFrame(loop);
  }

  const init = async () => {
    const stream = await getStream();
    if(stream){
      const videoTracks = stream.getVideoTracks();
      console.log(`Using video device: ${videoTracks[0].label}`);
      const {width, height} = videoTracks[0].getSettings();
      setCanvasBox({
        width: width ?? 0, 
        height: height ?? 0,
      })
      if(videoRef.current){
        videoRef.current.srcObject = stream;
        const ctx = canvasRef.current?.getContext('2d');
        if(ctx) draw(ctx);
      }
    }
  }

  useEffect(() => {
    init()
  }, [])
  
  
  

  return (
    <main
      className='w-screen h-screen flex flex-row'
    >
    
      <div className='h-full flex-1 flex flex-col items-center justify-center'>
        <canvas className="w-full" height={canvasBox.height} width={canvasBox.width} ref={canvasRef}></canvas>
        <video autoPlay playsInline ref={videoRef} hidden></video>
      </div>
      <div className='h-full flex-1 bg-white'>
      </div>
      
    </main>
  )
}
