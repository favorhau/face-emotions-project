import { Suspense } from 'react'
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
 
  return (
    <Canvas style={{height: 600, width: 500}}>
      
      <Suspense>
        <Model />
      </Suspense>
    </Canvas>
  )
}

useGLTF.preload('/assets/Wizardhat.glb');