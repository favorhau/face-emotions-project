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
    return <div className='h-28' 
            style={{
                height: device === 'h5' ? '3rem' : '',
                display: device === 'h5' ? 'flex' : '',
                justifyContent: 'center',
                position: 'fixed',
                width: '100%',
                zIndex: 99,
                background: bgColor === 'primary' ? '#3266E9' : ''
            }}
        >
        <Image width={device === 'pc' ? 200:140} 
                style={{padding: device === 'h5' ? 0 : '', transform: 'scale(0.8)',}} 
                height={device === 'pc' ? 64 : 16} 
                className='pl-6 pt-6 cursor-pointer' 
                alt='logo' 
                src={logo} 
                onClick={() => {

            window.location.href = '/'
        }}/>
    </div>
}