// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from 'next'
import { httpSlient } from '@/utils/requests';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { id } = req.query
  try{
    const ret = await httpSlient.get<ArrayBuffer>(`/api/img/${id}`, {responseType: 'arraybuffer'});
    res.setHeader('Content-Type', 'image/jpeg');
    res.setHeader('Cache-Control', 'public, max-age=31536000');

    res.status(200).send(ret)
  }catch (e){
    res.status(500).send('error');
  }
}
