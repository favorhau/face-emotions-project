import Image from "next/image"
import bg from '../../public/bg/backgroud.png'
import submitIcon from '../../public/assets/submitIcon.svg'
import Bar from "@/components/Bar"
import Hat from "@/components/Hat"
import { useState } from "react"

export default function Home() {
  const [id, setId] = useState<string>('') ;

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
          <div className="text-white text-6xl">
            <p>打开你的情绪世界</p>
            <p>Let Borderless</p>
            
            <div className="relative"> 
              <input
                className="w-full h-14 rounded-2xl mt-12 pl-6 text-black text-base" 
                placeholder="请输入 Atom ID" 
                maxLength={28} 
                style={{background: 'rgb(255,255,255,0.8)'}}
                onChange={(e) => {
                  setId(e.target.value);
                }}></input>
              {/* 跳转到 ID 页 */}
              <button 
                className="bg-primary absolute top-12 right-0 h-14 w-14 rounded-2xl flex justify-center items-center hover:scale-105 transition-all"
                onClick={() => {
                  window.location.href = `/user/${id}`
                }}>
                <Image width={24} height={24} alt="submit" src={submitIcon} />
              </button>
              <a className="underline text-primary text-sm mt-4" href="">创建 Atom ID</a>
            </div>
          </div>
          
          {/* 右边面板 */}
          <div className="w-100 h-100">
              <Hat />
          </div>
        </div>
        
      </div>
      <footer className="fixed bottom-10 left-36 text-white opacity-50 text-thin text-sm ">
          背景图由文心一格AI生成
        </footer>
    </main>
  )
}
