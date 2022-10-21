
// Modulos necesarios
import * as THREE from "../webgl/lib/three.module.js";
import {GLTFLoader} from "../webgl/lib/GLTFLoader.module.js";
import {OrbitControls} from "../webgl/lib/OrbitControls.module.js";
import {TWEEN} from "../webgl/lib/tween.module.js";
import {GUI} from "../webgl/lib/lil-gui.module.js";

// Variables estandar
let renderer, scene, camera, minimap;

// Otras globales
let cameraControls, effectController;
let track, car, finishLine, driverLocation, minimapFinish;
let keyboard;
let L = 800;

// globales de movimiento
let current_speed = 0;
let speedUp, breaking, turnLeft, turnRight;
let ghostTrack=[];
let prevLapCoords= []
let times = {
    best: 10000000,
    actual: 0,
    last: 0
}
let startLapTime, endLapTime = 0;


//user info
let selectedCar = 'ayrton_senna_f1'

const car_info = {
    'ayrton_senna_f1':{
        position: 1.75,
        maxSpeed: 2,
        scale: [0.20,0.20,0.20],
        rotation: [0,-Math.PI/2,0],
        lookAt: [0 ,0, -5]
    },
    'ferrari_246_f1':{
        position: 2,
        maxSpeed: 5,
        scale: [0.7,0.7,0.7],
        rotation: [0,Math.PI,0],
        lookAt: [5 ,0, 0]
    },
    'wheelchair':{
        position: 2,
        maxSpeed: 10,
        scale: [0.5,0.5,0.5],
        rotation: [0,0,0],
        lookAt: [-5 ,0, 0]
    },
    'jiotto_caspita_f1':{
        position: 0.5,
        maxSpeed: 4,
        scale: [0.7,0.7,0.7],
        rotation: [0,Math.PI/2,0]
    }
}

// Acciones
init();
loadScene();
// setupGUI();
render();

function init()
{
    // Instanciar el motor de render
    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth,window.innerHeight);
    document.getElementById('container').appendChild( renderer.domElement );
    renderer.antialias = true; //activar el antialiasing
    renderer.shadowMap.enabled = true

    renderer.setClearColor( new THREE.Color(0.2,0.2,0.2))
    renderer.autoClear = false;

    // Instanciar el nodo raiz de la escena
    scene = new THREE.Scene();
    //scene.background = new THREE.Color(0.5,0.5,0.5);

    // Onboard camera
    camera= new THREE.PerspectiveCamera(75,window.innerWidth/window.innerHeight,1,10000);
    camera.position.set(0.5,2,7);
    cameraControls = new OrbitControls( camera, renderer.domElement );
    cameraControls.target.set(0,1,0);
    camera.lookAt(0,1,0);
    
    //minimap  
    const aspectRatio = window.innerWidth/window.innerHeight;
    if(aspectRatio > 1){
        minimap = new THREE.OrthographicCamera(-L,L,L,-L,0,10000);
    }else{
        minimap = new THREE.OrthographicCamera(-L,L,L,-L,0,10000);
    }
    minimap.position.set(300,20,400);
    minimap.lookAt(300,0,400)

    //keyboard
    keyboard = new THREEx.KeyboardState();

    //Luces
    const ambiental = new THREE.AmbientLight(0xAAAAAA);
    scene.add(ambiental)

    // Eventos
    window.addEventListener('resize', updateAspectRatio );
    document.addEventListener('keydown', setDrive)
    document.addEventListener('keyup', unsetDrive)

}

function loadScene()
{
    drawFinishLine()
    loadTrack()
    loadCar(selectedCar)
}

function drawFinishLine(){
    const textureFloor = new THREE.TextureLoader().load('../webgl/images/finishLane.jpg')
    textureFloor.repeat.set(15,2)
    textureFloor.wrapS = textureFloor.wrapT = THREE.RepeatWrapping;
    const matFL = new THREE.MeshLambertMaterial({color: new THREE.Color("rgb(150,150,150)"), map:textureFloor})
    finishLine = new THREE.Mesh( new THREE.PlaneGeometry(70,15, 50,50), matFL );
    finishLine.rotation.z = -Math.PI/2
    finishLine.rotation.x = -Math.PI/2;
    finishLine.position.y = 1.4;
    finishLine.position.z = -0.5;
    finishLine.position.x = 5;
    finishLine.receiveShadow = true;
    scene.add(finishLine)
}

function loadTrack(){
    const glloader = new GLTFLoader();
    glloader.load('../webgl/models/tracks/circuit_race.glb',
    function(objeto)
    {
        track = objeto
        scene.add(objeto.scene);
        objeto.scene.traverse(ob => {
            if(ob.isObject3D){
                ob.castShadow = true;
            }
        })
        objeto.scene.scale.set(300,300,300);
        objeto.scene.position.y = 0;
        // objeto.scene.rotation.y = -Math.PI/2;
        objeto.scene.name = 'track';
        objeto.scene.receiveShadow = true;
        console.log(objeto);
    });
}

function loadCar(carName){
    const glloader = new GLTFLoader();
    glloader.load(`../webgl/models/cars/${carName}.glb`,
    function(objeto)
    {
        car = objeto.scene
        scene.add(objeto.scene);
        objeto.scene.traverse(ob => {
            if(ob.isObject3D){
                ob.castShadow = true;
            }
        })
        objeto.scene.scale.set(car_info[carName].scale[0],car_info[carName].scale[1],car_info[carName].scale[2]);
        objeto.scene.position.y = car_info[carName].position;
        objeto.scene.rotation.set(car_info[carName].rotation[0],car_info[carName].rotation[1],car_info[carName].rotation[2])
        objeto.scene.name = 'car';
        objeto.scene.receiveShadow = true;
        console.log(objeto);
        camera.position.set(car.position.x, camera.position.y+1, car.position.z)
        camera.lookAt(car_info[carName].lookAt[0],car_info[carName].lookAt[1],car_info[carName].lookAt[2]);
        car.add(camera)
        createMinimapObjects()

    });
}

function setDrive(event){
    if ( keyboard.eventMatches(event, 'a') || keyboard.eventMatches(event, 'left') ) {
        turnLeft = true
    }
    if ( keyboard.eventMatches(event, 'd') || keyboard.eventMatches(event, 'right') ) {
        turnRight = true
    }
    if ( keyboard.eventMatches(event, 's') || keyboard.eventMatches(event, 'down') ) {
        breaking = true
        speedUp = false
    }
    if ( keyboard.eventMatches(event, 'w') || keyboard.eventMatches(event, 'up') ) {
        speedUp = true
        breaking = false
    }
}

function unsetDrive(event){
    if ( keyboard.eventMatches(event, 'a') || keyboard.eventMatches(event, 'left') ) {
        turnLeft = false
    }
    if ( keyboard.eventMatches(event, 'd') || keyboard.eventMatches(event, 'right') ) {
        turnRight = false
    }
    if ( keyboard.eventMatches(event, 's') || keyboard.eventMatches(event, 'down') ) {
        breaking = false
    }
    if ( keyboard.eventMatches(event, 'w') || keyboard.eventMatches(event, 'up') ) {
        speedUp = false
    }
}

function createMinimapObjects(){
    driverLocation = new THREE.Mesh( new THREE.CylinderGeometry(50, 50, 1, 100, 2), new THREE.MeshBasicMaterial({color: 'red'}) )
    driverLocation.position.y = 50
    car.add(driverLocation)
    startLapTime = new Date()
}

// function setupGUI()
// {
// 	// Definicion de los controles
// 	effectController = {
// 		mensaje: 'Soldado & Robota',
// 		giroY: 0.0,
// 		separacion: 0,
// 		colorsuelo: "rgb(150,150,150)",
//         play: function(){video.play();},
//         pause: function(){video.pause()}
// 	};

// 	// Creacion interfaz
// 	const gui = new GUI();

// 	// Construccion del menu
// 	const h = gui.addFolder("Control esferaCubo");
// 	h.add(effectController, "mensaje").name("Aplicacion");
// 	h.add(effectController, "giroY", -180.0, 180.0, 0.025).name("Giro en Y");
// 	h.add(effectController, "separacion", { 'Ninguna': 0, 'Media': 2, 'Total': 5 }).name("Separacion");
//     h.add(effectController, 'play')
//     h.add(effectController, 'pause')
//     h.addColor(effectController, "colorsuelo").name("Color alambres");

// }

function updateAspectRatio()
{
    const ar = window.innerWidth/window.innerHeight;
    renderer.setSize(window.innerWidth,window.innerHeight);
    camera.aspect = ar;
    camera.updateProjectionMatrix();
}

// function animate(event)
// {
//     // Capturar y normalizar
//     let x= event.clientX;
//     let y = event.clientY;
//     x = ( x / window.innerWidth ) * 2 - 1;
//     y = -( y / window.innerHeight ) * 2 + 1;

//     // Construir el rayo y detectar la interseccion
//     const rayo = new THREE.Raycaster();
//     rayo.setFromCamera(new THREE.Vector2(x,y), camera);
//     const soldado = scene.getObjectByName('soldado');
//     const robot = scene.getObjectByName('robot');
//     let intersecciones = rayo.intersectObjects(soldado.children,true);

//     if( intersecciones.length > 0 ){
//         new TWEEN.Tween( soldado.position ).
//         to( {x:[0,0],y:[3,1],z:[0,0]}, 2000 ).
//         interpolation( TWEEN.Interpolation.Bezier ).
//         easing( TWEEN.Easing.Bounce.Out ).
//         start();
//     }

//     intersecciones = rayo.intersectObjects(robot.children,true);

//     if( intersecciones.length > 0 ){
//         new TWEEN.Tween( robot.rotation ).
//         to( {x:[0,0],y:[Math.PI,-Math.PI/2],z:[0,0]}, 5000 ).
//         interpolation( TWEEN.Interpolation.Linear ).
//         easing( TWEEN.Easing.Exponential.InOut ).
//         start();
//     }
// }

function update()
{
    if(car != undefined){
        checkLapLogic()
        if(speedUp){
            current_speed = Math.min(car_info[selectedCar].maxSpeed, current_speed + 0.1)
        }
        if(breaking){
            current_speed -= 0.05
        }
        if(!speedUp && !breaking){
            current_speed = Math.max(0, current_speed - 0.005)
        }
        if(turnLeft){
            car.rotation.y += Math.PI/180
            current_speed = current_speed>0? current_speed: 0.2;
        }
        if(turnRight){
            car.rotation.y -= Math.PI/180
            current_speed = current_speed>0? current_speed: 0.2;
        }
        // prevLapCoords.push(car.position)
        car.position.x += current_speed*(-Math.sin(car.rotation.y))
        car.position.z += current_speed*(-Math.cos(car.rotation.y))
        camera.updateProjectionMatrix()
    }


    // Lectura de controles en GUI (es mejor hacerlo con onChange)
	// cubo.position.set( -1-effectController.separacion/2, 0, 0 );
	// esfera.position.set( 1+effectController.separacion/2, 0, 0 );
	// cubo.material.setValues( { color: effectController.colorsuelo } );
	// esferaCubo.rotation.y = effectController.giroY * Math.PI/180;
    // TWEEN.update();
}

function checkLapLogic(){
    endLapTime = new Date()
    const elapsedTime = (endLapTime - startLapTime)/1000
    times.actual = elapsedTime;
    if(car.position.x > -2 && car.position.x < 14 && // has passed over finish lane
        car.position.z >-34 && car.position.z <34){
        if(Math.abs(elapsedTime) > 15 ){ //margin to not count while user is in finish lane
            times.last = elapsedTime;
            if (elapsedTime < times.best){
                times.best =  elapsedTime;
                // ghostTrack = [...prevLapCoords]
                //<div id="timerTop"><span id="timeCurrent">0.00</span></div>
                //const timerDisplay = document.getElementById("timeCurrent");
                //timerDisplay.innerText = (lap.times[0] / 1000).toFixed(2);
            }
            startLapTime = new Date();
            times.actual = 0;
            console.log(times)
        }
    }

}

function render()
{
    requestAnimationFrame(render);
    update();
    renderer.clear();
    renderer.setClearColor( new THREE.Color(0.2,0.2,0.2))
    renderer.setViewport(0,0,window.innerWidth, window.innerHeight);
    renderer.render(scene, camera);

    const newAspectRatio = window.innerWidth/window.innerHeight;
    let size = (newAspectRatio > 1)? window.innerHeight/3: window.innerWidth/3

    renderer.setClearColor( new THREE.Color(0.7,0.7,0.7))
    renderer.setViewport(0,window.innerHeight-size+1,size, size);
    renderer.render(scene,minimap);

    camera.updateProjectionMatrix();
    minimap.updateProjectionMatrix();

    TWEEN.update();
}