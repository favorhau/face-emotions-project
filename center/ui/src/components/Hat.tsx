import { Suspense, useEffect, useState } from 'react'
import { OrbitControls, OrthographicCamera, PerspectiveCamera, useGLTF } from '@react-three/drei';
import { Canvas, useFrame } from '@react-three/fiber';


function Model() {
  useFrame(({scene}) => {
    // This function runs at the native refresh rate inside of a shared render-loop
    scene.rotation.y -= 0.01
  })
  const result = useGLTF('/assets/Wizardhat.glb')
  return <>
    {/* <axesHelper/> */}
    <OrthographicCamera scale={0.9} position={[0, -2, 0]}>
      {/* <OrbitControls /> */}
      <primitive object={result.scene} />
      <ambientLight intensity={1.5}  position={[0, 0, 0 ]}/>
    </OrthographicCamera>
    
   
  </>

}

export default function Hat() {
 
 const [width, setWidth] = useState(1800);
 
 const updateWidth = () => {
  setWidth(window.innerWidth)
  console.log(window.innerWidth);
 }

 useEffect(() => {
  setWidth(window.innerWidth)
  addEventListener('resize', updateWidth)
  return () => {
    removeEventListener('resize', updateWidth); 
  }
 }, [])
 
  return (
    <Canvas style={{height: width > 640 ? 600 : 300, width: width > 640 ? 500 : 320}}>
      
      <Suspense>
        <Model />
      </Suspense>
    </Canvas>
  )
}

useGLTF.preload('/assets/Wizardhat.glb');