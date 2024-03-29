// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from 'next'
import { httpSlient } from '@/utils/requests';


type Data = {
  data: {
    result: boolean
  },
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  const  { code  } = req.body
  const ret = await httpSlient.post<Data>('/api/verify_code', {
    code
  });
  
  res.status(200).json(ret);
}
