import { Typography, CircularProgress, Box, IconButton, Backdrop } from '@mui/material';
import React, { useContext, useEffect, useRef, useState } from 'react';
import Image from 'next/image';
import SearchIcon from '@mui/icons-material/Search';
import BookmarkIcon from '@mui/icons-material/Bookmark';
import { httpClient } from '@/utils/requests';

type ReportListProps = Array<
    {
        name: string,
        id: string,
        grade: '优秀' | '良好' | '异常',
        date: string,
    }
>

export default function Reports(){
    const inputRef = useRef<HTMLInputElement>(null);
    const [list, setList] = useState<ReportListProps>();
    const [open, setOpen] = React.useState(false);
    const handleClose = () => {
      setOpen(false);
    };
    const handleOpen = () => {
      setOpen(true);
    };

    const init = async() => {
        const value = inputRef.current?.value;
        const data = await httpClient.post('/api/getReport', {
            id: value ? null : value,
        }) as unknown
        setList(
            [
                ...(data as ReportListProps).map(v=>{
                return {
                    name: v.name,
                    id: v.id,
                    grade: '优秀' as '优秀' | '良好' | '异常',
                    date: v.date,
                }
            })]
        )
    }
    
    const searchData = async () => {
        handleOpen()
        const value = inputRef.current?.value;
        const data = await httpClient.post('/api/getReport', {
            user_id: value,
            name: value,
            id: value,
        })
        setTimeout(() => {
            handleClose()
        }, 500) 
        setList(
            [
                ...(data as ReportListProps).map(v=>{
                return {
                    name: v.name,
                    id: v.id,
                    grade: '优秀' as '优秀' | '良好' | '异常',
                    date: v.date,
                }
            })]
        )
    }
    
    useEffect(() => {
        init()
    }, [])
    
    return <div className='w-full h-full flex flex-wrap text-black justify-start'>
       
       <Backdrop
        sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open={open}
        onClick={handleClose}
      >
        <CircularProgress color="inherit" />
      </Backdrop>
       <div className='w-full relative'>
        <input
            className="w-full h-14 rounded-2xl pl-6 text-black text-base border" 
            placeholder="搜索姓名、报告编号" 
            maxLength={28} 
            ref={inputRef}
            onKeyDown={(e) => {
                if (e.key === 'Enter') searchData()
            }}
            style={{background: 'rgb(255,255,255,0.8)'}}></input>
            <div className='absolute right-3 top-1/2 cursor-pointer' 
                style={{transform: 'translateY(-50%)'}}
                onClick={searchData}>
                <SearchIcon/>
            </div>
        </div>
        
        <div className='h-full mt-[2rem] flex flex-wrap'>
            {
                list && list.map(({name, id, grade, date}) => {
                    return <div
                        key={id}
                        className='min-w-[22rem] w-[45vw] shadow p-4 pb-10 mx-2 mb-4 rounded-xl flex items-center justify-between relative cursor-pointer'
                        onClick={() => {
                            window.location.href = `/report/${id}`
                        }}>
                        <div className='flex'>
                            <div className='rounded-full bg-black w-[3rem] h-[3rem]' style={{
                                background: id ? `url(/api/img/${id})` : '',
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