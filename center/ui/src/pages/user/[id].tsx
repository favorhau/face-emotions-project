import Bar from "@/components/Bar";
import { useRouter } from "next/router"
import * as React from 'react';
import Box from '@mui/material/Box';
import Tab from '@mui/material/Tab';
import TabContext from '@mui/lab/TabContext';
import TabList from '@mui/lab/TabList';
import TabPanel from '@mui/lab/TabPanel';
import Dashboard from "./compoents/Dashboard";
import Reports from "./compoents/Reports";
import Manager from "./compoents/Manager";


const Admin = () => {
  const [value, setValue] = React.useState('1');
  const [device, setDevice] = React.useState<'pc' | 'h5'>('pc');

  React.useEffect(() => {
    if(window.innerWidth <= 680){
      setDevice('h5');
    }
  }, [])
  
  const handleChange = (event: React.SyntheticEvent, newValue: string) => {
    setValue(newValue);
  };
  return <div className="w-full flex justify-center" style={{
    marginTop: device === 'h5' ? '4rem' : '8rem'
  }}>
    <Box  component="div" sx={{ width: '98%', typography: 'body1' }}>
      <TabContext value={value}>
        <Box  component="div" sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <TabList onChange={handleChange} aria-label="lab API tabs example">
            <Tab label="总览" value="1" />
            <Tab label="情绪报告" value="2" />
            <Tab label="用户管理" value="3" />
          </TabList>
        </Box>
        <TabPanel value="1">
          <Dashboard />
        </TabPanel>
        <TabPanel value="2">
          <Reports/>
        </TabPanel>
        <TabPanel value="3">
          <Manager/>
        </TabPanel>
      </TabContext>
      <footer className="mt-auto bottom-10 w-full flex justify-center my-8 text-black opacity-50 text-thin text-xs ">
        Copyright © 2023 Atom Go. All rights reserved.
      </footer>
    </Box>
  </div>
}

const User = () => {
  const router = useRouter()
  return <>
     <div className="flex flex-row w-full h-full">
        <div className="left-pan mt-60 ml-20 flex flex-col">
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
  </>
}
export default function UserContainer() {

  const router = useRouter()
  const [device, setDevice] = React.useState<'pc' | 'h5'>('pc');
  const {id} = router.query;

  React.useEffect(() => {
    if(window.innerWidth <= 680){
      setDevice('h5');
    }
  }, [])
  if(id === 'admin') return <main
    className='w-screen h-screen flex flex-col'
  ><Bar bgColor="primary" device={device}/><Admin/></main>
  else return  <main
    className='w-screen h-screen flex flex-col'
  ><Bar bgColor="primary" device={device}/><User/></main>
  
}
