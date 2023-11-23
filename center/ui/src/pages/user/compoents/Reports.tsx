import { Typography, CircularProgress, Box, IconButton } from '@mui/material';
import React, { useEffect, useState } from 'react';
import logo from '../../../../public/assets/device.jpg'
import Image from 'next/image';
import md5 from 'md5';
import SearchIcon from '@mui/icons-material/Search';
import BookmarkIcon from '@mui/icons-material/Bookmark';

type ReportListProps = Array<
    {
        name: string,
        id: string,
        grade: '优秀' | '良好' | '异常',
        imgData: string,
        date: string,
    }
>

export default function Reports(){
    
    const mock: ReportListProps = [
        {
            name: '戴景昊',
            id: '1',
            grade: '优秀',
            imgData: '',
            date: '2023-11-23',
        },
        {
            name: '戴景昊',
            id: '2',
            grade: '优秀',
            imgData: '',
            date: '2023-11-23',
        }
    ]
    const [list, setList] = useState<ReportListProps>(mock);

    useEffect(() => {
        
    }, [])
    
    const searchData = () => {
        
    }
    
    
    return <div className='w-full h-full flex flex-wrap text-black justify-start'>
       
       <div className='w-full relative'>
        <input
            className="w-full h-14 rounded-2xl pl-6 text-black text-base border" 
            placeholder="搜索姓名、报告编号" 
            maxLength={28} 
            style={{background: 'rgb(255,255,255,0.8)'}}></input>
            <div className='absolute right-3 top-1/2 cursor-pointer' 
                style={{transform: 'translateY(-50%)'}}
                onClick={searchData}>
                <SearchIcon/>
            </div>
        </div>
        
        <div className='h-full mt-[2rem] flex flex-wrap'>
            {
                list.map(({name, id, grade, imgData, date}) => {
                    return <div key={id} className='min-w-[22rem] w-[45vw] shadow p-4 pb-10 mx-2 mb-4 rounded-xl flex items-center justify-between relative cursor-pointer'>
                    <div className='flex'>
                        <div className='rounded-full bg-black w-[3rem] h-[3rem]' style={{
                            background: imgData ? `url(${imgData})` : 'gray',
                            backgroundPosition: 'center center',
                            backgroundSize: 'cover'
                        }}></div>
                        <div className='flex flex-col mx-[1rem]'>
                            <div className='text-black font-bold text-xl'>{name}</div>
                            <div className='text-invaild text-sm'>{date}</div>
                        </div>
                    </div>
                    <div className='text-success text-xl mx-4'>{grade}</div>
                    <hr className='w-full absolute bottom-[1.4rem] left-0 opacity-30'></hr>
                    <div className='absolute bottom-1  text-invaild text-[0.6rem] flex items-center uppercase'
                        ><BookmarkIcon style={{fontSize: 12}}/>
                        {id}
                    </div>

                </div>
                })
            }
        </div>
    </div>
}