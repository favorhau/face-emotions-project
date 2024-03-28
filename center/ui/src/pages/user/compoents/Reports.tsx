import { Typography, CircularProgress, Box, IconButton, Backdrop, Pagination, Stack, Button } from '@mui/material';
import React, { useContext, useEffect, useRef, useState } from 'react';
import Image from 'next/image';
import SearchIcon from '@mui/icons-material/Search';
import BookmarkIcon from '@mui/icons-material/Bookmark';
import { httpClient } from '@/utils/requests';
import { calHealthy, calHealthyText } from '@/utils/calculator';
import { ReportDataProps } from '@/pages/report/[id]';
import RefreshIcon from '@mui/icons-material/Refresh';
import { number } from 'echarts';

export type ReportListProps = Array<
    {
        name: string,
        id: string,
        grade: '优秀' | '良好' | '中等' | '异常',
        date: string,
        user_id: string,
        xlfxData?: Array<{
            [key: string]: number
        }>
    } 
>

export default function Reports(){
    const inputRef = useRef<HTMLInputElement>(null);
    const [list, setList] = useState<ReportListProps>();
    const [open, setOpen] = React.useState(false);
    const [currentPage, setCurrentPage] = useState(1);
    const [pageCount, setPageCount] = useState(1);
    const currPageSize = 0;
    const handleClose = () => {
      setOpen(false);
    };
    const handleOpen = () => {
      setOpen(true);
    };


    const init = async() => {
        const value = inputRef.current?.value;
        const {data , count, page, pageSize} = await httpClient.post('/api/getReport', {
            id: value ? null : value,
            page: currentPage,
            pageSize: currPageSize,
        }) as {
            data: ReportListProps,
            count: number,
            page: number
            pageSize: number,
        }
        
        setCurrentPage(1);
        setPageCount(count)
       
        setList(
            [
                ...(data as ReportListProps).map((v: any)=>{
                    const grade = calHealthyText(calHealthy(v['data']['心理分析'] as unknown as {name: string, value: number}[]));
                    return {
                        name: v.name,
                        id: v.id,
                        grade: grade,
                        user_id: v.user_id,
                        date: v.date,
                    }
            })]
        )
    }
    
    const handlePageChange = async (event: React.ChangeEvent<unknown>, value: number) => {
      setCurrentPage(value);
      const v = inputRef.current?.value;
      const {data , count, page, pageSize} = await httpClient.post('/api/getReport', {
        id: v ? null : v,
        page: value,
        pageSize: currPageSize,
        }) as {
            data: ReportListProps,
            count: number,
            page: number
            pageSize: number,
        }
        
        setPageCount(count);
    
        setList(
            [
                ...(data as ReportListProps).map((v: any)=>{
                    const grade = calHealthyText(calHealthy(v['data']['心理分析'] as unknown as {name: string, value: number}[]));
                    return {
                        name: v.name,
                        id: v.id,
                        grade: grade,
                        user_id: v.user_id,
                        date: v.date,
                    }
            })]
        )
    };
    
    const genReport =  async () => {
        handleOpen()
        await httpClient.post('/api/genReport') as unknown
        handleClose()
        
    }
    const searchData = async () => {
        handleOpen()
        const value = inputRef.current?.value;
        const {data , count, page, pageSize} = await httpClient.post('/api/getReport', {
            user_id: value,
            name: value,
            id: value,
            page: 1,
            pageSize: currPageSize,
        })  as {
            data: ReportListProps,
            count: number,
            page: number
            pageSize: number,
        }
        setPageCount(count);
        setTimeout(() => {
            handleClose()
        }, 500) 
        setList(
            [
                ...(data as ReportListProps).map((v: any)=>{
                const grade = calHealthyText(calHealthy(v['data']['心理分析'] as unknown as {name: string, value: number}[]));
                return {
                    name: v.name,
                    id: v.id,
                    grade: grade,
                    date: v.date,
                    user_id: v.user_id,
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
      <div 
      style={{zIndex: 999,}}
      className='fixed right-[2rem] bottom-[2rem] w-[8rem] h-[3rem] flex justify-center items-center rounded-full bg-primary transition-all hover:scale-105 cursor-pointer'
      onClick={() => {
        genReport()
      }}
        >
            <Button style={{color: 'white'}}>生成当天报告</Button> 
        </div>
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
        
        <div className='h-full mt-[2rem] flex flex-wrap justify-center'>
            {
                list && list.map(({name, id, grade, date, user_id}) => {
                    return <div
                        key={id}
                        className='min-w-[22rem] w-[45vw] shadow p-4 pb-10 mx-2 mb-4 rounded-xl flex items-center justify-between relative cursor-pointer'
                        onClick={() => {
                            window.location.href = `/report/${id}`
                        }}>
                        <div className='flex'>
                            <div className='rounded-full bg-black w-[3rem] h-[3rem]' style={{
                                background: id ? `url(/api/img/${user_id})` : '',
                                backgroundSize: 'cover'
                            }}></div>
                            <div className='flex flex-col mx-[1rem]'>
                                <div className='text-black font-bold text-xl'>{name}</div>
                                <div className='text-invaild text-sm'>{date}</div>
                            </div>
                        </div>
                        <div 
                            className='text-success text-xl mx-4'
                            style={{
                                color:
                                { '优秀': '#7CFFB2',
                                '良好': '#58D9F9',
                                '中等': '#FDDD60',
                                '异常': '#FF6E76'}[grade]
                            }}
                        >{grade}</div>
                        <hr className='w-full absolute bottom-[1.4rem] left-0 opacity-30'></hr>
                        <div className='absolute bottom-1  text-invaild text-[0.6rem] flex items-center uppercase'
                            ><BookmarkIcon style={{fontSize: 12}}/>
                            {id}
                        </div>

                </div>
                })
            }
            { pageCount > 0 && <Stack spacing={2} className='w-full flex justify-center items-center'>
                <Pagination onChange={handlePageChange} page={currentPage} className='mt-auto' count={pageCount} variant="outlined" color="primary" />
            </Stack> }
            { pageCount == 0 && <Stack spacing={2} className='w-full flex justify-center items-center'>
                <p>找不到数据</p>
            </Stack> }
        </div>
        
       
        
    </div>
}