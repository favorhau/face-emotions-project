/* eslint-disable @next/next/no-img-element */

export interface ReportDataProps{
  userId?: string,
  name?: string,
  date?: string,
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

import { useRouter } from "next/router";
import { useCallback, useEffect, useState } from "react";
import { httpClient } from "@/utils/requests";
import Bar from "@/components/Bar";
import { CircumplexCanvas, GaugeChart, LineChart, LineDataProps, Pie1Chart, Pie1DataProps, Pie2Chart, Pie2DataProps, Pie3Chart, Pie3DataProps, RadarChart, RadarDataProps } from "@/components/Chart";
import DenseTable from "@/components/Table";
import { calHealthy } from "../utils";

export default function Report() {

  const router = useRouter();

  const { id } = router.query;
  const [data, setData] = useState<ReportDataProps>({});

  //初始化report
  const init = useCallback(async () => {
    const ret = (await httpClient.post('/api/getReport', {
      id,
    }) as { [key: string]: any; data: { [key: string]: any; }; }[])[0];
    console.log(ret)
    setData({
      userId: ret.user_id as string,
      name: ret.name,
      date: ret.date,
      xlfxData: ret.data['心理分析'] as any,
      xlzxData: ret.data['心理走向'] as unknown as ReportDataProps['xlzxData'],
      qgfbData: ret.data['情感分布'] as unknown as ReportDataProps['qgfbData'],
      qgblData: ret.data['情感比例'] as unknown as ReportDataProps['qgblData'],
      hlzsData: ret.data['活力指数'] as unknown as ReportDataProps['hlzsData'],
    });
  }, [id]);
  const [device, setDevice] = useState<'pc' | 'h5'>('pc');

  useEffect(() => {
    if (window.innerWidth <= 680) {
      setDevice('h5');
    }
  }, []);

  useEffect(() => {
    if (id) init();
  }, [id, init]);

  return <main className='w-screen h-screen flex flex-col '>
    <Bar bgColor="primary" device={device} />
    <div className='h-full mt-32 flex flex-col justify-start items-center'>
      <div className="flex flex-col items-center">
        <div style={{
          background: `center / contain  url(/api/img/${data.userId})`,
        }} className="w-24 h-24 p-2 shadow-md rounded-full bg-cover" />
        <text className="text-black text-xl my-1">{data.name}</text>
        <text className="text-invaild text-sm">{data.date}</text>
        {data['xlfxData'] && <GaugeChart data={calHealthy(data['xlfxData'] as unknown  as { name: string; value: number; }[])} /> }
      </div>
      <div className="w-full flex flex-wrap justify-center">
        <div
          className='relative mx-[2rem] my-[2rem] min-w-[20rem] h-[20rem] w-[28vw] shadow p-10 ml-4 mb-4 rounded-xl flex flex-col items-center justify-center relative cursor-pointer'
        >
          <div className="text-black absolute left-[1rem] top-[1rem] flex items-center">
            <div className="bg-primary w-4 h-4 rounded-full mr-2"></div>情感比例
          </div>
          <Pie1Chart data={data['qgblData'] as unknown as Pie1DataProps['data']} />
        </div>
        <div
          className='relative mx-[2rem] my-[2rem] min-w-[20rem] h-[20rem] w-[28vw] shadow p-10 ml-4 mb-4 rounded-xl flex flex-col items-center justify-center relative cursor-pointer'
        >
          <div className="text-black absolute left-[1rem] top-[1rem] flex items-center">
            <div className="bg-error w-4 h-4 rounded-full mr-2"></div>情感分布
          </div>
          <Pie2Chart data={data['qgfbData'] as unknown as Pie2DataProps['data']} />
        </div>

        <div
          className='mx-[2rem] my-[2rem] min-w-[20rem] h-[20rem] w-[28vw] shadow p-10 ml-4 mb-4 rounded-xl flex flex-col items-center justify-center relative cursor-pointer'
        >
          <div className="text-black absolute left-[1rem] top-[1rem] flex items-center">
            <div className="w-4 h-4 rounded-full mr-2" style={{ background: 'green' }}></div>活力指数
          </div>
          <Pie3Chart data={data['hlzsData'] as unknown as Pie3DataProps['data']} />
        </div>

        <div className="flex flex-col flex-wrap">
          <div
            className='mx-[2rem] my-[2rem] min-w-[20rem] h-[20rem] w-[45vw] shadow p-10 ml-4 mb-4 rounded-xl flex flex-col items-center justify-center relative cursor-pointer'
          >

            <LineChart data={data['xlzxData'] as unknown as LineDataProps['data']} />
          </div>

          <div
            className='relative mx-[2rem] my-[2rem] min-w-[20rem] h-[30rem] w-[45vw] shadow p-10 ml-4 mb-4 rounded-xl flex flex-col items-center justify-center relative cursor-pointer'
          >
            <div className="text-black absolute left-[1rem] top-[1rem] flex items-center">
              <div className="w-4 h-4 rounded-full mr-2" style={{ background: 'yellow' }}></div>情绪模型
            </div>
            {/* 映射到 -20 ～ 20 */}
            {data.hlzsData && <CircumplexCanvas data={{
              activation: (data.hlzsData?.arousal ?? 0) / 10,
              pleasant: ((data.hlzsData?.pleasure ?? 0) - 200) / 10,
            }} />}
          </div>
        </div>

        <div
          className='mx-[2rem] my-[2rem] min-w-[20rem] h-[53rem] w-[45vw] shadow p-10 ml-4 mb-4 rounded-xl flex flex-col items-center justify-bewteen relative cursor-pointer'
        >
          <RadarChart data={data['xlfxData'] as unknown as RadarDataProps['data']} />
          <DenseTable data={data['xlfxData']?.map(v => v.value) as number[]} />
        </div>



      </div>

      <footer className="w-full flex justify-center my-[3rem] pb-[3rem] text-black opacity-50 text-thin text-xs ">
        Copyright © 2023 Atom Go. All rights reserved.
      </footer>
    </div>


  </main>;

}
