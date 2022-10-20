/* robot */

//required modules:
import * as THREE from "../webgl/lib/three.module.js";
import {OrbitControls} from "../webgl/lib/OrbitControls.module.js"
import {TWEEN} from "../webgl/lib/tween.module.js";
import {GUI} from "../webgl/lib/lil-gui.module.js";

//consensus globals
var renderer, scene, camera
let orthographicCamera

//globals
let cameraDriver;
let floor, robot, base, arm, foreArm, hand, pinLeft, pinRight;
const radius = 20;
const depth = 18;
const height = 120;
const segments = 35; 
let material;
let effectController;
var keyboard
var movement_dist = 5;

//texture globals
let ironMaterial, goldMaterial, shinyGoldMaterial;
let path, env;

let L = 100;

//Actions
init();
loadScene();
setupGUI();
render();

//init
function init(){
    //engine instance
    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.shadowMap.enabled = true;
    
    //insert canvas
    document.getElementById("container").appendChild(renderer.domElement);

    //avoid screen erase in each render()
    renderer.setClearColor( new THREE.Color(0.2,0.2,0.2))
    renderer.autoClear = false;

    //instance scene
    scene = new THREE.Scene();
    //scene.background = new THREE.Color(0.5, 0.5, 0.5);

    //main camera
    camera= new THREE.PerspectiveCamera(100,window.innerWidth/window.innerHeight,1,1000);
    const aspectRatio = window.innerWidth/window.innerHeight;
    camera.position.set(-80,250,-100);
    camera.lookAt(0, 125, 0);

    cameraDriver = new OrbitControls(camera, renderer.domElement);
    cameraDriver.target.set(0,1,0);

    //little camera
    if(aspectRatio > 1){
        orthographicCamera = new THREE.OrthographicCamera(-L,L,L,-L,0,300);
    }else{
        orthographicCamera = new THREE.OrthographicCamera(-L,L,L,-L,0,300);
    }
    orthographicCamera.position.set(0,240,0);
    orthographicCamera.lookAt(0,0,0)

    //keyboard
    keyboard = new THREEx.KeyboardState();
    renderer.domElement.setAttribute("tabIndex", "0");
    renderer.domElement.focus();

    const ambiental = new THREE.AmbientLight(0x555555);
    scene.add(ambiental)

    const focal = new THREE.SpotLight(0xFFFFFF, 0.7);
    focal.position.set(150, 350, 150);
    focal.target.position.set(0,150,0);
    focal.shadow.camera.near = 0.5;
    focal.shadow.camera.far = 1000 
    focal.angle = Math.PI/5
    focal.penumbra = 0.3
    focal.castShadow = true
    focal.shadow.camera.fov = 80
    scene.add(focal)
    scene.add(new THREE.CameraHelper(focal.shadow.camera))

    const puntual = new THREE.PointLight(0xFFFFFFF, 0.3);
    puntual.position.set(200,100,-50);
    puntual.castShadow  =true
    scene.add(puntual);

    const directional = new THREE.DirectionalLight(0xFFFFFF, 0.5);
    directional.position.set(-150,250,75); //vector L
    directional.target.position.set( 0, 100, 0 );
    directional.shadow.camera.near = 0.5;
    directional.shadow.camera.far = 500  
    directional.shadowCameraLeft = -350;
    directional.shadowCameraRight = 350;
    directional.shadowCameraTop = 350;
    directional.shadowCameraBottom = -350;
    directional.castShadow = true
    scene.add(directional);
    scene.add(new THREE.CameraHelper(directional.shadow.camera))
    directional.target.updateMatrixWorld()

    //listeners
    window.addEventListener('resize', updateAspectRatio);
    document.addEventListener('keydown', moveRobot)
}

function loadScene(){
    material = new THREE.MeshNormalMaterial({wireframe: false})

    path = '../webgl/images/'

    env = [
        path + 'posx.jpg', 
        path + 'negx.jpg',
        path + 'posy.jpg', 
        path + 'negy.jpg',
        path + 'posz.jpg', 
        path + 'negz.jpg'
    ]
    
    const walls = []
    for (let index = 0; index < env.length; index++) {
        const element = env[index];
        walls.push(new THREE.MeshBasicMaterial({side: THREE.BackSide, map: new THREE.TextureLoader().load(element)}))
    }
    const geoRoom = new THREE.BoxGeometry(1000,1000,1000);
    const room = new THREE.Mesh(geoRoom, walls)
    scene.add(room)

    //Robot creation
    robot = new THREE.Object3D();
    
    //1-base
    const baseTex = new THREE.TextureLoader().load(path+'metal_128.jpg')
    ironMaterial = new THREE.MeshLambertMaterial({color:'gray', map: baseTex});

    base = new THREE.Object3D()
    base.add(new THREE.Mesh( new THREE.CylinderGeometry(50, 50, 15, segments, 15), ironMaterial ))
    robot.add(base);

    //2-robot arm
    arm = new THREE.Object3D();
    base.add(arm)
    createArm()

    //3-robot forearm
    const forearmTex = new THREE.TextureLoader().load(path+'gold_256.jpg')
    goldMaterial = new THREE.MeshLambertMaterial({color:'white', map: forearmTex});
    shinyGoldMaterial = new THREE.MeshPhongMaterial({color:'white',specular: 'white', shininess: 30, map: forearmTex});
    foreArm = new THREE.Object3D();
    arm.add(foreArm)
    createForeArm()
    
    robot.rotateY(Math.PI/2)

    scene.add(robot);

    robot.traverse(
        function (child){
            if(child instanceof THREE.Mesh){
                child.castShadow = true
                child.receiveShadow = true 
            }
        }
    )

    //floor
    const floorTex = new THREE.TextureLoader().load(path+'pisometalico_1024.jpg')
    floorTex.repeat.set(4,4)
    floorTex.wrapS = floorTex.wrapT = THREE.RepeatWrapping;
    const matFloor = new THREE.MeshLambertMaterial({map:floorTex})
    floor = new THREE.Mesh( new THREE.PlaneGeometry(1000, 1000, 25, 25), matFloor);
    floor.rotateX(-Math.PI/2); // floor.rotate.x = -Math.PI/2
    scene.add(floor);
    floor.position.y = -0.2;
    floor.receiveShadow = true

    scene.add(new THREE.AxesHelper(3));
}

function render(){
    requestAnimationFrame(render);
    renderer.clear();

    renderer.setClearColor( new THREE.Color(0.2,0.2,0.2))
    renderer.setViewport(0,0,window.innerWidth, window.innerHeight);
    renderer.render(scene, camera);

    const newAspectRatio = window.innerWidth/window.innerHeight;
    let size = (newAspectRatio > 1)? window.innerHeight/4: window.innerWidth/4

    renderer.setClearColor( new THREE.Color(0.7,0.7,0.7))
    renderer.setViewport(0,window.innerHeight-size+1,size, size);
    renderer.render(scene,orthographicCamera);

    TWEEN.update();
    
}

function createArm(){
    //define sphere material
    
    const textArt = new THREE.CubeTextureLoader().load(env)
    const matArt = new THREE.MeshPhongMaterial({color: 'white', specular: 'gray', shininess: 30, envMap: textArt})

    const axis = new THREE.Mesh( new THREE.CylinderGeometry(radius, radius, depth, segments, 15), ironMaterial )
    axis.rotateX(-Math.PI/2)
    const armBar = new THREE.Mesh( new THREE.BoxGeometry(12, height, depth), ironMaterial )
    armBar.position.y = height/2;
    const articulation = new THREE.Mesh( new THREE.SphereGeometry(radius, segments/2, segments/2), matArt )
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

function updateAspectRatio(){
    /* code for Perspective cameras */
    //set frame size
    renderer.setSize(window.innerWidth, window.innerHeight)
    
    //compute aspect ratio
    const newAspectRatio = window.innerWidth/window.innerHeight;

    //update view perspective camera
    camera.aspect = newAspectRatio;
    camera.updateProjectionMatrix();
    orthographicCamera.updateProjectionMatrix();

}

function setupGUI()
{
	// Definicion de los controles
	effectController = {
		giroBase: 90,
		giroBrazo: 0.0,
		giroYAntebrazo: 0.0,
		giroZAntebrazo: 0.0,
		giroPinza: 0.0,
		separacionPinza: 10,
        alambres: false,
        animate: animate
	};

	// Creacion interfaz
	const gui = new GUI();

	// Construccion del menu
	const h = gui.addFolder("Control Robot");
	h.add(effectController, "giroBase", -180.0, 180.0, 0.025).name("Giro Base");
	h.add(effectController, "giroBrazo", -45.0, 45.0, 0.025).name("Giro Brazo");
	h.add(effectController, "giroYAntebrazo", -180.0, 180.0, 0.025).name("Giro Antebrazo Y");
	h.add(effectController, "giroZAntebrazo", -90.0, 90.0, 0.025).name("Giro Antebrazo Z");
	h.add(effectController, "giroPinza", -40.0, 220.0, 0.025).name("Giro Pinza");
	h.add(effectController, "separacionPinza", 0, 15.0, 0.025).name("Separacion pinza");
	h.add(effectController, "alambres").name("Alambres");
    h.add(effectController, "animate").name("Animar")
    h.onChange(update)

}

function update(){

	robot.rotation.y = effectController.giroBase * Math.PI/180;
    arm.rotation.z = effectController.giroBrazo * Math.PI/180;
    foreArm.rotation.y = effectController.giroYAntebrazo * Math.PI/180
    foreArm.rotation.z = effectController.giroZAntebrazo * Math.PI/180
    hand.rotation.z = effectController.giroPinza * Math.PI/180
    robot.traverse(
        function (child){
            if(child instanceof THREE.Mesh){
                child.material = new THREE.MeshNormalMaterial({wireframe: effectController.alambres})
            }
        }
    )
    pinLeft.position.z = ( effectController.separacionPinza/2 -5);
    pinRight.position.z = ( - effectController.separacionPinza/2 +5);
    floor.material = new THREE.MeshNormalMaterial({wireframe: effectController.alambres})
}

function moveRobot (event) {
    if ( keyboard.eventMatches(event, 'a') || keyboard.eventMatches(event, 'left') ) {
        robot.position.x += movement_dist;
    }
    if ( keyboard.eventMatches(event, 'd') || keyboard.eventMatches(event, 'right') ) {
        robot.position.x -= movement_dist;
    }
    if ( keyboard.eventMatches(event, 's') || keyboard.eventMatches(event, 'down') ) {
        robot.position.z -= movement_dist;
    }
    if ( keyboard.eventMatches(event, 'w') || keyboard.eventMatches(event, 'up') ) {
        robot.position.z += movement_dist;
    }
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
