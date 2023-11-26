import { styled } from '@mui/material/styles';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell, { tableCellClasses } from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { useEffect, useCallback, useState, useRef, useLayoutEffect } from 'react';
import { CircularProgress, Backdrop, Dialog, Typography, Button, Stack, Fade, Box, Alert, IconButton, Collapse } from '@mui/material';
import { httpClient } from '@/utils/requests';
import AddIcon from '@mui/icons-material/Add';
import TextField from '@mui/material/TextField';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import { LocalizationProvider, TimePicker } from '@mui/x-date-pickers';
import dayjs from 'dayjs';
import TrapFocus from '@mui/material/Unstable_TrapFocus';
import CloseIcon from '@mui/icons-material/Close';

const StyledTableCell = styled(TableCell)(({ theme }) => ({
  [`&.${tableCellClasses.head}`]: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  [`&.${tableCellClasses.body}`]: {
    fontSize: 14,
  },
}));

const StyledTableRow = styled(TableRow)(({ theme }) => ({
  '&:nth-of-type(odd)': {
    backgroundColor: theme.palette.action.hover,
  },
  // hide last border
  '&:last-child td, &:last-child th': {
    border: 0,
  },
}));

export interface ManagerProps{
  data: {
    name: string,
    id: number,
    startTime: number,
    endTime: number,
  }[]
}

export default function Manager() {

  const [rows, setRows] = useState<ManagerProps['data']>([]);
  const [open, setOpen] = useState(false);
  const [addFormShow, setAddFormShow] = useState(false);
  const [showImg, setShowImg] = useState(false);
  const [id, setId] = useState(0);
  const [formData, setFormData] = useState({
    name: '',
    startTime: dayjs(),
    endTime: dayjs(),
    img: '',
  });
  const [bannerOpen, setBannerOpen] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [alOpenConfig, setAlOpenConfig] = useState({
    open: false,
    content: '',
  });
  
  const handleClose = () => {
    setOpen(false);
  };
  const handleOpen = () => {
    setOpen(true);
  };
  

  const init = useCallback(async () => {
    handleOpen()
    const data = await httpClient.post('/api/getUsers', {}) as ManagerProps['data']
    setRows(data);
    setTimeout(() => {
      handleClose()
    }, 300);
    
  }, [])
  
  const handleFileChange = () => {
    const file = fileInputRef.current?.files?.[0]
    if(file){
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        const base64String = reader.result as string;
        setFormData((f) => {
          return {
            ...f,
            img: base64String?.split(',')[1]
          }
        })
      };
    }
  }

  const addUser = async () => {
    if(Object.values(formData).every(v => v ? true : false)){
      if(formData.startTime < formData.endTime){
        const payload = {
          ...formData,
          startTime: formData.startTime.format('HH:mm:ss'),
          endTime: formData.endTime.format('HH:mm:ss'),
        }
        handleOpen()
        const ret = await httpClient.post('/api/addUsers', payload)
        if(ret){
         setAddFormShow(false);
        }
        init()
        handleClose()
      }else{
        setAlOpenConfig(() => {
          return {
            content: '开始时间要早于结束时间',
            open: true,
          }
        });
      }
    }else{
      setAlOpenConfig(() => {
        return {
          content: '请填写完整信息',
          open: true,
        }
      });
    }
  }
  
  useEffect(() => {
    init()
  }, [init])
  
  
  useLayoutEffect(() => {
  
    fileInputRef.current?.addEventListener('change',handleFileChange);
    
    return () => {
      removeEventListener('change', handleFileChange)
    }
  }, [])
  
  return (
    <> 
    
    <TrapFocus open disableAutoFocus disableEnforceFocus>
        <Fade appear={false} in={bannerOpen}>
          <Paper
            role="dialog"
      
            aria-modal="false"
            aria-label="Cookie banner"
            square
            variant="outlined"
            tabIndex={-1}
            sx={{
              position: 'fixed',
              bottom: 0,
              left: 0,
              right: 0,
              m: 0,
              p: 2,
              borderWidth: 0,
              borderTopWidth: 1,
              zIndex: 999
            }}
          >
            <Stack
              direction={{ xs: 'column', sm: 'row' }}
              justifyContent="space-between"
              gap={2}
            >
              <Box
                component="div"
                sx={{
                  flexShrink: 1,
                  alignSelf: { xs: 'flex-start', sm: 'center' },
                }}
              >
                <Typography fontWeight="bold">删除操作不可回退</Typography>
                <Typography variant="body2">
                  确定删除吗
                </Typography>
              </Box>
              <Stack
                gap={2}
                direction={{
                  xs: 'row-reverse',
                  sm: 'row',
                }}
                sx={{
                  flexShrink: 0,
                  alignSelf: { xs: 'flex-end', sm: 'center' },
                }}
              >
                <Button size="small" onClick={
                    () => {
                      httpClient.post('/api/delUsers', {id: id}).then(() => {
                        setBannerOpen(false);
                        init()
                      })
                      
                    }
                  } variant="contained">
                  确定
                </Button>
                <Button size="small" onClick={() => setBannerOpen(false)}>
                  取消
                </Button>
              </Stack>
            </Stack>
          </Paper>
        </Fade>
      </TrapFocus>
    <Backdrop
        sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open={open}
        onClick={handleClose}
      >
      <CircularProgress color="inherit" />
    </Backdrop>
    <Dialog fullScreen={false} open={showImg} onClose={() => setShowImg(false)} >
      <div className='w-[20rem] h-[20rem]' style={{background: `center / contain  url(/api/img/${id}) no-repeat`}}></div>
    </Dialog>
    <Dialog fullScreen={false} open={addFormShow} onClose={() => setAddFormShow(false)}>
      <div className='w-[40vw] min-w-[20rem] h-[36rem] flex flex-col items-center'>
        <Typography variant='h4' className='py-[2rem]'> 添加用户 </Typography>
        <Stack spacing={2}>
          <div className='w-full flex justify-center'>
            <div 
              className='w-[6rem] h-[6rem] bg-white shadow rounded-full flex justify-center items-center cursor-pointer'
              style={{
                background: `center / contain  url(data:image/jpeg;base64,${formData.img}) no-repeat`
              }}
              onClick={() => {
                fileInputRef.current?.click()
              }}
              >
              {!formData.img && <span className='text-sm'> 上传人脸</span> }
            </div>
          </div>
          <TextField
            label="姓名"
            id="outlined-size-small"
            size="small"
            defaultValue={formData.name}
            onChange={(n) => {
              setFormData((f: any)=> {
                  return {
                    ...f,
                    name: n.target.value
                  }
              })
            }}
          />
          <LocalizationProvider dateAdapter={AdapterDayjs}>
          <TimePicker label="开始检测时间" 
            defaultValue={formData.startTime} 
            timeSteps={{minutes: 5}}
            onChange={(n) => {
              setFormData((f: any)=> {
                  return {
                    ...f,
                    startTime: n?.set('second', 0)
                  }
              })
            }}/>
          <TimePicker 
            label="结束检测时间" 
            defaultValue={formData.endTime} 
            timeSteps={{minutes: 5}}
            onChange={(n) => {
              setFormData((f: any)=> {
                  return {
                    ...f,
                    endTime: n?.set('second', 0)
                  }
              })
            }}
          />
          </LocalizationProvider>
          <Button 
            variant='outlined' 
            onClick={()=>{
              addUser()
            }}
          >
              提交
          </Button>
          <Collapse in={alOpenConfig.open}>
      <Alert
        severity="error"
        action={
          <IconButton
            aria-label="close"
            color="inherit"
            size="small"
            onClick={() => {
              setAlOpenConfig((v) => {
                return {
                  ...v,
                  open: false,
                }
              });
            }}
          >
            <CloseIcon fontSize="inherit" />
          </IconButton>
        }
        sx={{ mb: 2 }}
      >
        {alOpenConfig.content}
      </Alert>
    </Collapse>
        </Stack>
        
      </div>
    </Dialog>
    <input type="file" ref={fileInputRef} id="fileInput" className='hidden' accept="image/jpeg"/>

    <div 
      className='fixed right-[2rem] bottom-[2rem] w-[3rem] h-[3rem] flex justify-center items-center rounded-full bg-primary transition-all  hover:scale-105 cursor-pointer'
      onClick={() => {
        setAddFormShow(true);
      }}
    >
      <AddIcon />
    </div>
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 200 }} aria-label="customized table">
        <TableHead>
          <TableRow>
            <StyledTableCell>id</StyledTableCell>
            <StyledTableCell align="right">姓名</StyledTableCell>
            <StyledTableCell align="right">开始检测时间</StyledTableCell>
            <StyledTableCell align="right">结束检测时间</StyledTableCell>
            <StyledTableCell align="right">操作</StyledTableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <StyledTableRow key={row.name}>
              <StyledTableCell component="th" scope="row">
                {row.id}
              </StyledTableCell>
              <StyledTableCell align="right">{row.name}</StyledTableCell>
              <StyledTableCell align="right">{row.startTime}</StyledTableCell>
              <StyledTableCell align="right">{row.endTime}</StyledTableCell>
              <StyledTableCell align="right"><a href='#' className='text-primary' 
                  onClick={() => {
                  setId(row.id)
                  setShowImg(true);
                }}>查看</a>
                <a href='#' className='text-error ml-2'
                 onClick={() => {
                  setId(row.id)
                  setBannerOpen(true);
                 }}
                >删除</a>
              </StyledTableCell>
            </StyledTableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer></>
  );
}
