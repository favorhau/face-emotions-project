import { Suspense } from 'react'
import { OrbitControls, useGLTF } from '@react-three/drei';
import { Canvas, useFrame } from '@react-three/fiber';


function Model() {
  useFrame(({scene}) => {
    // This function runs at the native refresh rate inside of a shared render-loop
    scene.rotation.y -= 0.01
  })
  const result = useGLTF('/assets/Wizardhat.glb')
  return <>
    <axesHelper/>
    <OrbitControls />
    <ambientLight intensity={1.5}  position={[0, 0, 0 ]}/>
    <perspectiveCamera position={[0, 100, 200]}></perspectiveCamera>
    <primitive object={result.scene} />
  </>

}

export default function Hat() {
 
  return (
    <Canvas style={{height: 600, width: 600}}>
      <Suspense>
        <Model />
      </Suspense>
    </Canvas>
  )
}

useGLTF.preload('/assets/Wizardhat.glb');