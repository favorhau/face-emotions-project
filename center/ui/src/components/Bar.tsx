import { useEffect, useState } from 'react';
import logo from '../../public/assets/logo.png'
import Image from 'next/image'

/* 顶部栏 */

interface BarProps{
    bgColor?: 'primary' | 'none',
    device?: 'pc' | 'h5'
}
export default function Bar(props: BarProps){
    
    const { bgColor = 'none', device='pc' } = props;
    const [currentPageType, setCurrentPageType]  = useState<'homepage' | 'others'>('homepage');
    
    useEffect(() => {
        if(window.location.pathname.includes('report')){
            setCurrentPageType('others')
        }
    }, []);
    return <div className='h-28 flex justify-between items-center' 
            style={{
                height: device === 'h5' ? '3rem' : '',
                display: device === 'h5' ? 'flex' : '',
                justifyContent: device === 'h5' ? 'center' : 'between',
                flexDirection:  device === 'pc' ? 'row' : 'column',
                position: 'fixed',
                width: '100%',
                zIndex: 99,
                background: bgColor === 'primary' ? '#3266E9' : ''
            }}
        >
        <Image width={device === 'pc' ? 200:150} 
                style={{padding: device === 'h5' ? 0 : '', transform: 'scale(0.8)',}} 
                height={device === 'pc' ? 64 : 16} 
                className='pl-6 pt-2 cursor-pointer' 
                alt='logo' 
                src={logo} 
                onClick={() => {

            window.location.href = '/'
        }}/>
        {currentPageType == 'homepage' && <span style={{
            display: device === 'h5' ? 'none' : '',
        }} className='cursor-default pr-8'>打开情绪世界</span> }
        {currentPageType == 'others' && <span style={{
            display: device === 'h5' ? 'none' : '',
        }} className='cursor-pointer pr-8' onClick={() => {window.location.href = '/user/admin'}}>返回首页</span> }
    </div>
}