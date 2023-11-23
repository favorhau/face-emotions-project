import { useEffect } from "react"

export default function Blank(){
    useEffect(() => {
        location.href = '/'
    })
    return <div className="text-black w-full h-screen text-2xl flex justify-center items-center">
        页面为空 即将自动跳转
    </div>
}