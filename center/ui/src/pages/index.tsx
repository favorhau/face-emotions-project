import Image from "next/image"
import bg from '../../public/bg/backgroud.png'
import submitIcon from '../../public/assets/submitIcon.svg'
import Bar from "@/components/Bar"
import Hat from "@/components/Hat"
import { LegacyRef, useEffect, useRef, useState } from "react"
import { httpClient } from "@/utils/requests"
import { Alert, Stack } from "@mui/material"

export default function Home() {

  const [showAlert, setShowAlert] = useState(false);
  
  const inputRef = useRef<HTMLInputElement>(null);
  const handleLogin = async (code: string) => {
    const {data: {result}} = await httpClient.post('/api/verifyCode', {
      code
    }) as { data: {result: boolean} }
    if(result){
      window.location.href = '/user/admin'
    }else{
      setShowAlert(true);
      setTimeout(() => setShowAlert(false), 1000);
    }
  }
  
  return (
    <main
      className='w-screen h-screen flex flex-row'
    >
      {/* 图像蒙层 */}
      <Image src={bg} className="h-screen w-screen blur-sm object-cover fixed top-0 left-0" alt="background"></Image>
      {/* 表面蒙层 */}
      <div className="fixed top-0 left-0 w-screen h-screen">
        <Bar />
        <div className="relative w-5/6 h-full flex flex-row justify-between mt-40 flex-wrap" style={{left: '50%', transform: 'translate(-50%)'}}>
          {/* 左边面板 */}
          <div className="text-white text-4xl lg:text-6xl sm:text-4xl">
            <p>打开你的情绪世界</p>
            <p>Let Borderless</p>
            
            <div className="relative"> 
              <input
                className="w-full h-14 rounded-2xl mt-12 pl-6 text-black text-base" 
                placeholder="请输入 TOTP 登录验证码" 
                maxLength={28}
                ref={inputRef}
                style={{background: 'rgb(255,255,255,0.8)'}}
                onKeyDown={(e) => {
                  const code = inputRef.current?.value;
                  if (e.key === 'Enter') handleLogin(code??'');
                }}></input>
              {/* 跳转到 ID 页 */}
              <button 
                className="bg-primary absolute top-12 right-0 h-14 w-14 rounded-2xl flex justify-center items-center hover:scale-105 transition-all"
                onClick={() => {
                  const code = inputRef.current?.value
                  handleLogin(code??'');
                }}>
                <Image width={24} height={24} alt="submit" src={submitIcon} />
              </button>
            </div>
          </div>
          
          {/* 右边面板 */}
          <div className="w-100 h-100" style={{transform: 'translateY(-20vh)'}}>
              <Hat />
          </div>
        </div>
        
      </div>
      
      <Stack style={{
        opacity: showAlert ? 1 : 0
      }} className="fixed bottom-0 text-white transition-all" sx={{ width: '100%' }} spacing={2}>
        <Alert severity="error">登录 TOTP 验证码错误</Alert>
      </Stack>
     
      <footer className="fixed left-1/2 -translate-x-1/2 w-4/5 text-center md:left-64 bottom-10 lg:left-64 sm:left-1/2 text-white opacity-50 text-thin text-xs">
        Copyright © 2023 Atom Go. All rights reserved.
        </footer>
    </main>
  )
}
