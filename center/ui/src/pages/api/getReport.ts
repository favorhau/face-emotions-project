// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from 'next'
import axios from 'axios';
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
  const  { user_id, id, name  } = req.body
  const ret = await httpSlient.post<Data>('/api/get_report', {
    user_id,
    id,
    name
  });
  
  
  res.status(200).json(ret.data);
}
