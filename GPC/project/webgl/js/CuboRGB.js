/**
* CuboRGB.js
* Seminarios GPC #2. Ejemplo de uso de BufferGeometry
*   En sentido antihorario las caras son:
*   Delante:   7,0,3,4
*   Derecha:   0,1,2,3
*   Detras:    1,6,5,2
*   Izquierda: 6,7,4,5
*   Arriba:    3,2,5,4
+   Abajo:     0,7,6,1
* Donde se han numerado de 0..7 los vertices del cubo.
* Dado que cada vertice solo tiene un color el buffer de
* coordenadas y el de colores son de 8x3=24 floats.
* Los indices indican como formar los triangulos (6cx2tx3v=36)
*
* @author <rvivo@upv.es>, 2022
*/

// Modulos necesarios
import * as THREE from "../lib/three.module.js";

// Globales
let renderer, scene, camera, cubo;
let angulo = 0.01;

// Acciones
init();
loadCubo(1.0);
render();

function init()
{
  renderer = new THREE.WebGLRenderer();
  renderer.setSize( window.innerWidth, window.innerHeight );
  renderer.setClearColor( new THREE.Color(0xFFFFFF) );
  document.getElementById('container').appendChild( renderer.domElement );

  scene = new THREE.Scene();

  var aspectRatio = window.innerWidth / window.innerHeight;
  camera = new THREE.PerspectiveCamera( 40, aspectRatio , 0.1, 100 );
  camera.position.set( 1, 1.5, 2 );
  camera.lookAt( new THREE.Vector3( 0, 0, 0 ) );

  window.addEventListener('resize', updateAspectRatio );
}

function loadCubo(lado)
{
  // Instancia el objeto BufferGeometry
	const malla = new THREE.BufferGeometry();
  // Construye la lista de coordenadas y colores por vertice
  const semilado = lado/2.0;
  const coordenadas = [ // 8vert x3coor = 24float
  semilado,-semilado, semilado,
  semilado,-semilado,-semilado,
  semilado, semilado,-semilado,
  semilado, semilado, semilado,
 -semilado, semilado, semilado,
 -semilado, semilado,-semilado,
 -semilado,-semilado,-semilado,
 -semilado,-semilado, semilado  ];
  const colores = [ // 8 x 3 = 24
  1,0,0,   
  1,0,1,
  1,1,1,
  1,1,0,
  0,1,0,
  0,1,1,
  0,0,1,
  0,0,0  ];

  const indices = [ // 6caras x 2triangulos x3vertices = 36
  0,3,7, 7,3,4, 0,1,2, 
  0,2,3, 4,3,2, 4,2,5,
  6,7,4, 6,4,5, 1,5,2,
  1,6,5, 7,6,1, 7,1,0     ];

  // Geometria por att arrays en r140
  malla.setIndex( indices );
  malla.setAttribute( 'position', new THREE.Float32BufferAttribute(coordenadas,3));
  malla.setAttribute( 'color', new THREE.Float32BufferAttribute(colores,3));

  // Configura un material
  const material = new THREE.MeshBasicMaterial( { vertexColors: true } );

  // Construye el objeto grafico 
  console.log(malla);   //-> Puedes consultar la estructura del objeto
  cubo = new THREE.Mesh( malla, material );

	// Añade el objeto grafico a la escena
	scene.add( cubo );
}

function updateAspectRatio()
{
  renderer.setSize(window.innerWidth, window.innerHeight);
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
}

function update()
{
  // rotacion acumulativa
	cubo.rotateOnAxis( new THREE.Vector3(0,1,0), angulo );
}

function render()
{
	requestAnimationFrame( render );
	update();
	renderer.render( scene, camera );
}