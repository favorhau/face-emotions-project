import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

function createData(
  name: string,
  grade: number,
  interval: string,
  comment: string,
) {
  return { name, grade, interval, comment };
}

export default function DenseTable(props: {data: number[]}) {

  const {data} = props;

  const c1 = ["关怀", "戒备", "同理心", "恐慌", "自杀倾向", "情绪稳定", "社交期望", "躁动", "药物使用"];
  const c2 = [[-20, 20], [10, 30], [0, 40], [20, 50], [0, 50], [0, 80], [20, 40], [10, 40], [20, 60]];
 
  const c3 = data?.map((c, idx) => {
    const g = (c - c2[idx][0]) / (c2[idx][1] - c2[idx][0]);
    if(g <= 0.2){
      return '低'
    }else if(g > 0.2 && g <= 0.8){
      return '普通'
    }else if(g > 0.8 && g <= 1){
      return '高'
    }else{
      return '极高'
    }
  })
   
  const rows = [
    ...data?.map((v, idx) => {
      return createData(c1[idx], v, c2[idx].join("-"), c3[idx]);
    }) ?? []
  ]
  
  
  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 100 }} size="small" aria-label="a dense table">
        <TableHead>
          <TableRow>
            <TableCell className='font-bold'>项目</TableCell>
            <TableCell className='font-bold' align="right">得分</TableCell>
            <TableCell className='font-bold' align="right">正常范围</TableCell>
            <TableCell className='font-bold' align="right">评价</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow
              key={row.name}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                {row.name}
              </TableCell>
              <TableCell align="right">{row.grade}</TableCell>
              <TableCell align="right">{row.interval}</TableCell>
              <TableCell align="right">{row.comment}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer> 
  ); 
}