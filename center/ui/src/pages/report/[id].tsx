/* eslint-disable @next/next/no-img-element */
import { useRouter } from "next/router"
import axios from "axios";
import { useEffect, useState } from "react";
import { httpClient } from "@/utils/requests";
import Bar from "@/components/Bar";


interface ReportDataProps{
  userId?: string,
  name?: string,
  xlfxData?: Array<{
    [key: string]: number
  }>
  xlzxData?: {
    arousal: number[],
    pleasure: number[],
    timeInterval: string,
  }
  qgfbData?:Array<{
    [key: string]: number
  }> 
  qgblData?: Array<{
    [key: string]: number
  }> 
  hlzsData?: {
    arousal: number,
    pleasure: number
  }
}

export default function Report() {

  const router = useRouter();
  
  const {id} = router.query;
  const [data, setData] = useState<ReportDataProps>({})
  
  //初始化report
  const init = async () => {
    const data = await httpClient.post('/api/getReport', {
      id,
    }) as ReportDataProps
    setData(data);
  }
  const [device, setDevice] = useState<'pc' | 'h5'>('pc');

  useEffect(() => {
    if(window.innerWidth <= 680){
      setDevice('h5');
    }
  }, [])
  useEffect(() => {
    init()
  }, [])
  
  return  <main className='w-screen h-screen flex flex-col '>
    <Bar bgColor="primary" device={device}/>
  </main>

}