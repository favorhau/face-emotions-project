// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from 'next'
import axios from 'axios';


type Data = {
  ret: string
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {

  const {data} = req.body;
  
  const ret = await axios.post('http://127.0.0.1:8080/api/test', {
    data: data,
  });
  
  res.status(200).json(ret.data)
}
