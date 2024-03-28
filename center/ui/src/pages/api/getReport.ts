// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from 'next'
import { httpSlient } from '@/utils/requests';


type Data = {
  data: {
    [key: string]: string,
  },
  count: number,
  page: number
  pageSize: number,
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  const  { user_id, id, name, type, page, pageSize  } = req.body
  const ret = await httpSlient.post<Data>('/api/get_report', {
    user_id,
    id,
    name,
    type,
    page,
    pageSize
  });
  
  res.status(200).json(ret);
}
