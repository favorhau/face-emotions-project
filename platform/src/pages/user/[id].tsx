import Bar from "@/components/Bar";
import { useRouter } from "next/router"
import { useEffect, useRef, useState } from "react"

export default function User() {

  const router = useRouter()
  const {id} = router.query;

  useEffect(() => {
  }, [])
  

  return (
    <main
      className='w-screen h-screen flex flex-col '
    >
      <Bar bgColor={'primary'}></Bar>
    
      <div className="flex flex-row w-full h-full">
        <div className="left-pan mt-40 ml-20 flex flex-col">
          <p className="text-black text-4xl">您总共有7项情绪报告</p>
          
          <button className="bg-primary text-xl rounded-xl h-16 w-48 mt-6"
            onClick={() => {
              router.push('/report/111')
            }}> 
            生成报告 
          </button>
          
          <p className="text-primary mt-8 font-bold">查看总览</p>
        </div>
        
        <div className="right-pan">
          
        </div>
      </div>
    </main>
  )
}
