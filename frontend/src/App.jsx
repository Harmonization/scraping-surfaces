import { useState, useEffect, useRef, Fragment } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import * as THREE from 'three'

function Surface({ points }) {
  
  useEffect(() => {
    const tempObject = new THREE.Object3D()

    points.forEach((point, id) => {
      tempObject.position.set(...point)
      tempObject.updateMatrix()
      mref.current.setMatrixAt(id, tempObject.matrix);
    })
    mref.current.instanceMatrix.needsUpdate = true;
    
  }, [points])
  const mref = useRef()

  return (
    <instancedMesh ref={mref} args={[null, null, points.length]}>
      <sphereGeometry/>
      <meshStandardMaterial color={'hotpink'} opacity={.7}/>
    </instancedMesh>
  )
}

function Card({ name, latex, image, text, link, active, indx, setActive }) {

  const cardClick = () => {
    if (!active) {
      console.log(name)
      setActive(indx)
    }
  }

  return (
    <div className="card" onClick={cardClick} active={active ? '1' : '0'} id={`card-${indx}`}>
      <div className="info">
        <h2 className='name'>{name}</h2>
        <img src={latex} alt="latex" className='latex'/>
        <img src={image} alt="image" className='image'/>
        <p className='text'>{text} <a href={link} target='_blank'>...читать далее</a></p> 
      </div>
    </div>
  )
}

function Cards({ data, loading, active, setActive }) {
  const {name, latex_img, img, text, link} = data

  return (
    <>
      {loading ? 'Загрузка данных с сервера' : name.map((name_i, i) => 
        <Card
          name={name_i}
          latex={latex_img[i]}
          image={img[i]}
          text={text[i]}
          link={link[i]}
          active={active === i ? true : false} 
          indx={i} 
          setActive={setActive}
          key={`card-${i}`}
        />
        )
      }
    </>
  )
}

function App() {
  const [loading, setLoading] = useState(true)
  const [data, setData] = useState({})
  const [active, setActive] = useState(-1)

  const [points, setPoints] = useState([])
  const [parameters, setParameters] = useState({})


  const getData = async () => {
    const response = await fetch(`http://127.0.0.1:8000/api/surface/`)
    if (!response.ok) { throw new Error('Запрос не сработал') }
    setData(await response.json())
    setLoading(false)
  }

  const getPoints = async () => {
    if (active === -1) return

    const canvas = document.querySelector('.canvas')
    const card_i = document.getElementById(`card-${active}`)
    card_i.after(canvas)

    const response = await fetch(`http://127.0.0.1:8000/api/surface/?indx=${active}`)
    if (!response.ok) { throw new Error('Запрос не сработал') }
    const { parameters, points: newPoints} = await response.json()
    setParameters(parameters)
    setPoints(newPoints)
  }

  const changeParams = ({ target }) => {
    const name = target.getAttribute('param')
    setParameters(parameters => ({...parameters, [name]: target.value}))
  }

  const leaveFocus = async () => {
    const response = await fetch(`http://127.0.0.1:8000/api/surface/?indx=${active}`, {
      method: 'POST',
      body: JSON.stringify(parameters)
    })
    if (!response.ok) { throw new Error('Запрос не сработал') }
    const { points: newPoints } = await response.json()
    setPoints(newPoints)
  }

  useEffect(() => {getData()}, [])
  useEffect(() => {getPoints()}, [active])

  return (
    <>
     {active !== -1 && 
     <div className="canvas">
      {points.length !== 0 &&
        <div className="parameters">
          {active !== -1 && Object.entries(parameters).map(([param, value], i) => 
            <div className="parameter" key={`parameter-${i}`}>
              <label htmlFor={`parameter-${i}`}>{param}</label>
              <input 
                id={`parameter-${i}`} 
                type="number" 
                step="0.1" 
                param={param} 
                value={value} 
                onChange={changeParams} 
                onBlur={leaveFocus}
                onKeyDown={({key}) => {key === 'Enter' && leaveFocus()}}/>
            </div>
          )}
      </div>}
      {points.length !== 0 &&
        <Canvas camera={{position: [65, 65, 65]}}>
          <ambientLight />
          <OrbitControls enableZoom={true} />
          <axesHelper args={[100]} />
          <Surface points={points}/>
        </Canvas>}
    </div>}
    <Cards data={data} loading={loading} active={active} setActive={setActive}/>
    </>
  )
}

export default App