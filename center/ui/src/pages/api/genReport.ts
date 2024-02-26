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
  const ret = await httpSlient.post<Data>('/api/gen_report');
  
  res.status(200).json(ret.data);
}
