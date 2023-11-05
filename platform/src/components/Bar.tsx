import logo from '../../public/assets/logo.png'
import Image from 'next/image'

/* 顶部栏 */

interface BarProps{
    bgColor?: 'primary' | 'none'
}
export default function Bar(props: BarProps){

    const { bgColor = 'none' } = props;
    return <div className='w-full h-28' 
            style={{
            background: bgColor === 'primary' ? '#3266E9' : ''}}
        >
        <Image width={200} height={64} className='pl-6 pt-6 cursor-pointer' alt='logo' src={logo} onClick={() => {
            window.location.href = '/'
        }}/>
    </div>
}