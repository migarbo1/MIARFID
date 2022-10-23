
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
let track, car, finishLine, driverLocation;
let keyboard;
let L = 800;

let floor, robot, base, arm, foreArm, hand, pinLeft, pinRight, path;
let ironMaterial, goldMaterial, shinyGoldMaterial;
const radius = 20;
const depth = 18;
const height = 120;
const segments = 35; 

// globales de movimiento
let current_speed = 0;
let speedUp, breaking, turnLeft, turnRight;
let ghostTrack=[];
let prevLapCoords= []
let times = {
    best: 0,
    actual: 0,
    last: 0
}
let startLapTime, endLapTime = 0;
let isInPause = false;
let isInControls = true;
let elapsedTime = 0

//user info
let selectedCar = 'ayrton_senna_f1'
let carsFanzone = []
let carNames = ['ayrton_senna_f1', 'wheelchair', 'jiotto_caspita_f1']

const car_info = {
    'ayrton_senna_f1':{
        position: 1.75,
        scale: [0.20,0.20,0.20],
        rotation: [0,-Math.PI/2,0],
        lookAt: [0 ,0, -5],
        indicatorSize: 50,
        cameraPos: 1,
        maxSpeed: 2,
        turnAngle: Math.PI/130,
        acceleration: 0.15,
        brakeForce: 0.05
    },
    'wheelchair':{
        position: 2,
        scale: [0.5,0.5,0.5],
        rotation: [0,0,0],
        lookAt: [5 ,0, 0],
        indicatorSize: 20,
        cameraPos: 1,
        maxSpeed: 2.2,
        turnAngle: Math.PI/110,
        acceleration: 0.075,
        brakeForce: 0.03
    },
    'jiotto_caspita_f1':{
        position: 1.7,
        scale: [0.7,0.7,0.7],
        rotation: [0,Math.PI/2,0],
        lookAt: [0 ,0, 5],
        indicatorSize: 20,
        cameraPos: 0.5,
        maxSpeed: 1.4,
        turnAngle: Math.PI/180,
        acceleration: 0.1,
        brakeForce: 0.04
    }
}

// Acciones
init();
loadScene();
setupGUI();
render();

setInterval(() => {
    animate()
}, 10000);

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

    initScene()

    // Eventos
    window.addEventListener('resize', updateAspectRatio );
    document.addEventListener('keydown', setDrive)
    document.addEventListener('keyup', unsetDrive)

}

function initScene(){
    // Instanciar el nodo raiz de la escena
    scene = new THREE.Scene();
    //scene.background = new THREE.Color(0.5,0.5,0.5);

    // Onboard camera
    createOnboardCamera()
    
    //minimap  
    const aspectRatio = window.innerWidth/window.innerHeight;
    if(aspectRatio > 1){
        minimap = new THREE.OrthographicCamera(-L,L,L,-L,-5,10000);
    }else{
        minimap = new THREE.OrthographicCamera(-L,L,L,-L,-5,10000);
    }
    minimap.position.set(300,50,400);
    minimap.lookAt(300,0,400)

    //keyboard
    keyboard = new THREEx.KeyboardState();

    //Luces
    const ambiental = new THREE.AmbientLight(0x333333, 0.3);
    scene.add(ambiental)
}

function incTime(){
    if(!isInPause){
        elapsedTime +=0.01
    }
}

setInterval(() => {incTime()},10)

function circuitLights(){
    const cameraPositions = [[-600,300,150],[900, 300, 100]]//,[0, 400, -300]]
    const cameraLookats = [[-300,0,150],[600,0,100]]//,[0,0,300]]
    for (let index = 0; index < cameraPositions.length; index++) {
        const pos = cameraPositions[index];
        const target =cameraLookats[index] 
        const focal = new THREE.SpotLight(0xFFFFFF, 0.6);
        focal.position.set(pos[0], pos[1], pos[2]);
        focal.target.position.set(target[0], target[1], target[2]);
        focal.target.updateMatrixWorld();
        focal.shadow.camera.near = 0.5;
        focal.shadow.camera.far = 700
        focal.angle = Math.PI/5
        focal.penumbra = 0.3
        focal.castShadow = true
        focal.shadow.camera.fov = 65
        scene.add(focal)
    }
}

function loadScene()
{
    
    loadingLogic()
    circuitLights()
    drawBackground()
    drawFinishLine()
    loadTrack()
    loadCar(selectedCar)
    loadSceneAnimatedObjects()
}

function loadingLogic(){
    document.getElementById("loading").style.display = "flex"; 
    document.getElementById("container").style.display = "none"; 
    times = {
        best: 0,
        actual: 0,
        last: 0
    }
}

function drawBackground(){
    const env = [
        '../webgl/images/Yokohama3/posx.jpg', 
        '../webgl/images/Yokohama3/negx.jpg',
        '../webgl/images/Yokohama3/posy.jpg', 
        '../webgl/images/Yokohama3/negy.jpg',
        '../webgl/images/Yokohama3/posz.jpg', 
        '../webgl/images/Yokohama3/negz.jpg'
    ]
    
    const walls = []
    for (let index = 0; index < env.length; index++) {
        const element = env[index];
        walls.push(new THREE.MeshBasicMaterial({side: THREE.BackSide, map: new THREE.TextureLoader().load(element)}))
    }
    const geoRoom = new THREE.BoxGeometry(1600,1700,1700);
    const room = new THREE.Mesh(geoRoom, walls)
    room.position.y = -50
    scene.add(room)
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
                ob.castShadow = false;
                ob.receiveShadow = true;
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

function createOnboardCamera(){
    camera= new THREE.PerspectiveCamera(75,window.innerWidth/window.innerHeight,1,10000);
    camera.position.set(0.5,2,7);
    camera.lookAt(0,1,0);
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
        objeto.scene.castShadow = true;
        console.log(objeto);
        camera.position.set(car.position.x, camera.position.y+car_info[carName].cameraPos, car.position.z)
        camera.lookAt(car_info[carName].lookAt[0],car_info[carName].lookAt[1],car_info[carName].lookAt[2]);
        car.add(camera)
        createMinimapObjects()
    });
}

function setDrive(event){
    if(!isInPause && !isInControls){
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
    console.log(event)
    if(keyboard.eventMatches(event, 'escape')){
        if(isInPause){play()}else{pause()}
    }
    if(event.key == 'Enter'){
        isInControls = false;
        document.getElementById("container").style.display = "block"; 
        document.getElementById("controls").style.display = "none"; 
    }
}

function unsetDrive(event){
    if(!isInPause){
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
}

function createMinimapObjects(){
    driverLocation = new THREE.Mesh( new THREE.CylinderGeometry(car_info[selectedCar].indicatorSize, car_info[selectedCar].indicatorSize, 1, 100, 2), new THREE.MeshBasicMaterial({color: 'red'}) )
    driverLocation.position.y = 50
    car.add(driverLocation)
    document.getElementById("loading").style.display = "none"; 
    if(isInControls){
        document.getElementById("controls").style.display = "flex"; 
    }else{
        document.getElementById("container").style.display = "block"; 
    }
    //startLapTime = new Date()
}

function loadSceneAnimatedObjects(){
    
    //Robot creation
    robot = new THREE.Object3D();
    
    path = '../webgl/images/'

    //1-base
    const baseTex = new THREE.TextureLoader().load(path+'metal_128.jpg')
    ironMaterial = new THREE.MeshLambertMaterial({color:'gray', map: baseTex});

    base = new THREE.Object3D()
    base.add(new THREE.Mesh( new THREE.CylinderGeometry(50, 50, 15, segments, 15), ironMaterial ))
    robot.add(base);

    //2-robot arm
    const forearmTex = new THREE.TextureLoader().load(path+'gold_256.jpg')
    goldMaterial = new THREE.MeshLambertMaterial({color:'white', map: forearmTex});
    arm = new THREE.Object3D();
    base.add(arm)
    createArm()

    //3-robot forearm
    shinyGoldMaterial = new THREE.MeshPhongMaterial({color:'white',specular: 'white', shininess: 30, map: forearmTex});
    foreArm = new THREE.Object3D();
    arm.add(foreArm)
    createForeArm()
    
    robot.rotateY(Math.PI/2)

    robot.scale.set(0.2,0.2,0.2)

    scene.add(robot);

    robot.traverse(
        function (child){
            if(child instanceof THREE.Mesh){
                child.castShadow = true
                child.receiveShadow = true 
            }
        }
    )
    robot.position.set(536.44,1.75,64.61)
        
    animate()

}
function createArm(){
    //define sphere material

    const axis = new THREE.Mesh( new THREE.CylinderGeometry(radius, radius, depth, segments, 15), ironMaterial )
    axis.rotateX(-Math.PI/2)
    const armBar = new THREE.Mesh( new THREE.BoxGeometry(12, height, depth), ironMaterial )
    armBar.position.y = height/2;
    const articulation = new THREE.Mesh( new THREE.SphereGeometry(radius, segments/2, segments/2), goldMaterial )
    articulation.position.y = height;
    arm.add(axis);
    arm.add(armBar);
    arm.add(articulation);
    return arm;
}

function createForeArm() {
    for (let index = 0; index < 4; index++) {
        const bar = new THREE.Mesh( new THREE.BoxGeometry(4, 80, 4), goldMaterial );
        bar.matrixAutoUpdate = false;
        var mt = new THREE.Matrix4();
        var mr = new THREE.Matrix4();
        mt.makeTranslation(8,40,-8);
        mr.makeRotationY(index*Math.PI/2);
        bar.matrix = mr.multiply(mt)
        foreArm.add(bar);
    }

    const base = new THREE.Mesh( new THREE.CylinderGeometry(radius+2, radius+2, 6, 20, 20), goldMaterial );
    foreArm.add(base);

    hand = new THREE.Object3D();
    hand.position.y = 80;
    foreArm.add(hand);
    const hand_cylinder = new THREE.Mesh( new THREE.CylinderGeometry(15,15,40, 20, 20), shinyGoldMaterial )
    hand_cylinder.rotateX(-Math.PI/2);

    hand.add(hand_cylinder)
    createBothFingers()

    foreArm.position.y = height;

}

function createBothFingers(){ 
    pinLeft = createFinger()
    pinLeft.rotateX(-Math.PI/2)
    pinLeft.position.z = 0;
    hand.add(pinLeft)

    pinRight = createFinger()
    pinRight.rotateX(Math.PI/2)
    pinRight.position.z = 0;
    hand.add(pinRight)
}

function createFinger(){
    const fingerText = new THREE.TextureLoader().load(path+'black_iron_256.jpg')
    const blackIronMaterial = new THREE.MeshPhongMaterial({color:'white', specular: 'white', shininess: 30, map: fingerText});
    const coords = [ //10 caras * 4 vertices * 3 coord = 120float
        //big rectangle top X
        0, -8, -10, //0 -- 0
        0, -8, 10, //2 -- 1
        19, -8, 10, //3 -- 2
        19, -8, -10, //1 -- 3
        
        //big rectangle front
        
        //big rectangle bottom X
        0, -12, 10, //6 -- 4
        0, -12, -10, //4 -- 5
        19, -12, -10, //5 -- 6
        19, -12, 10, //7 -- 7
        
        //big rectangle back X
        0, -8, 10, //2 -- 8
        0, -8, -10, //0 -- 9
        0, -12, -10, //4 -- 10
        0, -12, 10, //6 -- 11

        //big rectangle left X
        19, -8, 10, //3 -- 12
        0, -8, 10, //2 -- 13
        0, -12, 10, //6 -- 14
        19, -12, 10, //7 -- 15
        
        //big rectangle right X
        0, -8, -10, //0 -- 16
        19, -8, -10, //1 -- 17
        19, -12, -10, //5 -- 18
        0, -12, -10, //4 -- 19

        //polygon top X
        19, -8, -10, //1 -- 20
        19, -8, 10, //3 -- 21
        38, -8, 5, //10 -- 22
        38, -8, -5, //8 -- 23
        
        //polygon front X
        38, -8, -5, //8 -- 24
        38, -8, 5, //10 -- 25
        38, -10, 5, //11 -- 26  
        38, -10, -5, //9 -- 27
        
        //polygon bottom X
        19, -12, 10, //7 -- 28
        19, -12, -10, //5 -- 29
        38, -10, -5, //9 -- 30
        38, -10, 5, //11 -- 31 
        
        //polygon left X
        38, -8, 5, //10 -- 32
        19, -8, 10, //3 -- 33
        19, -12, 10, //7 -- 34
        38, -10, 5, //11 -- 35 
        
        //polygon right X
        19, -8, -10, //1 -- 36
        38, -8, -5, //8 -- 37
        38, -10, -5, //9 -- 38
        19, -12, -10 //5 -- 39
    ]

    const norms = [ //10 caras * 4 vertices * 3 coord = 120float
    //big rectangle top X
    0,1,0, 0,1,0, 0,1,0, 0,1,0,
    
    //big rectangle front
    
    //big rectangle bottom X
    0,-1,0, 0,-1,0, 0,-1,0, 0,-1,0,
    
    //big rectangle back X
    0,0,-1, 0,0,-1, 0,0,-1, 0,0,-1,

    //big rectangle left X
    0,0,1, 0,0,1, 0,0,1, 0,0,1,
    
    //big rectangle right X
    0,0,-1, 0,0,-1, 0,0,-1, 0,0,-1,

    //polygon top X
    0,1,0, 0,1,0, 0,1,0, 0,1,0,
    
    //polygon front X
    1,0,0, 1,0,0, 1,0,0, 1,0,0,
    
    //polygon bottom X
    2,-19,0, 2,-19,0, 2,-19,0, 2,-19,0,  
    
    //polygon left X
    5,0,19, 5,0,19, 5,0,19, 5,0,19, 
    
    //polygon right X
    5,0,-19, 5,0,-19, 5,0,-19, 5,0,-19
    
]     

    const indexes = [
        //big rectangle top
        0,1,2,
        2,3,0,

        //big rectangle front

        //big rectangle bottom
        4,5,6,
        6,7,4,

        //big rectangle back
        8,9,10,
        10,11,8,

        //big rectangle left
        12,13,14,
        14,15,12,

        //big rectangle right
        16,17,18,
        18,19,16,

        //polygon top
        20,21,22,
        22,23,20,

        //polygon front
        24,25,26,
        26,27,24,

        //polygon bottom
        28,29,30,
        30,31,28,

        //polygon left
        32,33,34,
        34,35,32,

        //polygon right
        36,37,38,
        38,39,36
    ]

    const finger = new THREE.BufferGeometry();
    finger.setIndex(indexes);
    finger.setAttribute("position", new THREE.Float32BufferAttribute(coords,3));
    finger.setAttribute("normal", new THREE.Float32BufferAttribute(norms,3));
    return new THREE.Mesh(finger, blackIronMaterial); 

}

function setupGUI()
{
	// Definicion de los controles
	effectController = {
		carSelector: 0,
        // play: function(){play();},
        // pause: function(){pause()}
	};

	// Creacion interfaz
	const gui = new GUI();

	// Construccion del menu
	const h = gui.addFolder("User Settings");
	h.add(effectController, "carSelector", { 'ayrton_senna_f1': 0, 'jiotto_caspita_f1': 2, 'Especial': 1 }).name("Car");
    // h.add(effectController, 'play')
    // h.add(effectController, 'pause')
    h.onChange(applyChanges)

}

function play(){
    if(isInPause){
        document.getElementById("pause").style.display = "none"; 
        document.getElementById("container").style.display = "block"; 
        isInPause = false;
    }
}

function pause(){
    if(!isInPause){
        isInPause = true;
        document.getElementById("pause").style.display = "block"; 
        document.getElementById("container").style.display = "none"; 
    }
}

function applyChanges(){
    selectedCar = carNames[effectController.carSelector]
    renderer.domElement.focus()
    initScene()
    loadScene()
}

function updateAspectRatio()
{
    const ar = window.innerWidth/window.innerHeight;
    renderer.setSize(window.innerWidth,window.innerHeight);
    camera.aspect = ar;
    camera.updateProjectionMatrix();
}

function animate(){
    new TWEEN.Tween(robot.rotation)
        .to({x: [0,0,0,0], y:[-Math.PI, Math.PI, Math.PI/2], z:[0,0,0,0]}, 10000)
        .easing(TWEEN.Easing.Sinusoidal.InOut)
        .start()
    new TWEEN.Tween(arm.rotation)
        .to({x: [0,0,0,0], y:[0,0,0,0], z:[-Math.PI/4, Math.PI/4, 0]}, 10000)
        .easing(TWEEN.Easing.Sinusoidal.InOut)
        .start()
    new TWEEN.Tween(foreArm.rotation)
        .to({x: [0,0,0,0], y:[-Math.PI, Math.PI, 0], z:[-Math.PI/2, Math.PI/2, 0]}, 10000)
        .easing(TWEEN.Easing.Sinusoidal.InOut)
        .start()
    new TWEEN.Tween(hand.rotation)
        .to({x: [0,0,0,0], y:[0,0,0,0], z:[-40*Math.PI/180, 220*Math.PI/180, 0]}, 10000)
        .easing(TWEEN.Easing.Sinusoidal.InOut)
        .start()
    new TWEEN.Tween(pinLeft.position)
        .to({x: [0,0,0,0], y:[0,0,0,0], z:[-5, 7.5, 0]}, 10000)
        .easing(TWEEN.Easing.Sinusoidal.InOut)
        .start()
    new TWEEN.Tween(pinRight.position)
        .to({x: [0,0,0,0], y:[0,0,0,0], z:[5, -7.5, 0]}, 10000)
        .easing(TWEEN.Easing.Sinusoidal.InOut)
        .start()
}

function update()
{
    if(!isInPause){
        if(car != undefined){
            checkLapLogic()
            if(speedUp){
                current_speed = Math.min(car_info[selectedCar].maxSpeed, current_speed + car_info[selectedCar].acceleration)
            }
            if(breaking){
                current_speed -= car_info[selectedCar].brakeForce
            }
            if(!speedUp && !breaking){
                current_speed = Math.max(0, current_speed - 0.005)
            }
            if(turnLeft){
                car.rotation.y += car_info[selectedCar].turnAngle
                current_speed = current_speed>0? current_speed: 0.2;
            }
            if(turnRight){
                car.rotation.y -= car_info[selectedCar].turnAngle
                current_speed = current_speed>0? current_speed: 0.2;
            }
            // prevLapCoords.push(car.position)
            switch (selectedCar) {
                case 'ayrton_senna_f1':
                    car.position.x += current_speed*(-Math.sin(car.rotation.y))
                    car.position.z += current_speed*(-Math.cos(car.rotation.y))
                    break;
            
                case 'jiotto_caspita_f1':
                    car.position.x -= current_speed*(-Math.sin(car.rotation.y))
                    car.position.z -= current_speed*(-Math.cos(car.rotation.y))
                    break;
    
                case 'wheelchair':
                    car.position.x -= current_speed*(-Math.cos(-car.rotation.y))
                    car.position.z -= current_speed*(-Math.sin(-car.rotation.y))
                    break;
            }
            camera.updateProjectionMatrix()
            rotateWheels()
        }
    }
}

function rotateWheels(){
    car.traverse(ob => {
        if(ob instanceof THREE.Mesh){
            if(ob.name == 'Object_17'){
                ob.material.map.rotation += current_speed*Math.PI/180 //"works"
            }
        }
    })
}

function checkLapLogic(){
    //endLapTime = new Date()
    //const elapsedTime = (endLapTime - startLapTime)/1000 //TODO: change by a setTimeout that checks if its in pause or not
    times.actual = elapsedTime;
    const current = document.getElementById("timeCurrent");
    const diff = document.getElementById("diff");
    const best = document.getElementById("bestTime");
    if(car.position.x > -2 && car.position.x < 14 && // has passed over finish lane
    car.position.z >-34 && car.position.z <34){
        if(Math.abs(elapsedTime) > 5 ){ //margin to not count while user is in finish lane
            times.last = elapsedTime;
            if (elapsedTime < times.best || times.best == 0){
                times.best =  elapsedTime;
                // ghostTrack = [...prevLapCoords]
                diff.innerText = ' (+0.00)'
                best.innerText = (times.best).toFixed(2);
            }else{
                diff.innerText = "( +" + (elapsedTime-times.best).toFixed(2)+')';
            }
        }
        //startLapTime = new Date();
        elapsedTime = 0
        times.actual = 0;
    }
    current.innerText = (times.actual).toFixed(2);

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