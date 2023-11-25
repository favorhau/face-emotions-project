// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from 'next'
import { httpSlient } from '@/utils/requests';


type Data = {
  data: {
    [key: string]: string,
  }
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data['data']>
) {
const  { name, startTime, endTime, img  } = req.body;
  const ret = await httpSlient.post<Data>('/api/add_users', {
    name, startTime, endTime, img
  });
  
  res.status(200).json(ret.data);
}
