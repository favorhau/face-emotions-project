import Image from "next/image"
import mountains from '../../public/bg/backgroud.png'

export default function Home() {

  return (
    <main
      className='w-screen h-screen flex flex-row'
    >
      <Image src={mountains} className="h-screen w-screen object-fit" alt="background"></Image>
    </main>
  )
}
