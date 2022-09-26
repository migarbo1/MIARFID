/* robot */

//required modules:
import * as THREE from "../webgl/lib/three.module.js";
import {GLTFLoader} from "../webgl/lib/GLTFLoader.module.js";

//consensus globals
var renderer, scene, camera

//globals
let robot;
const radius = 20;
const depth = 18;
const height = 120;
const segments = 35; 
let material;

//Actions
init();
loadScene();
render();

//init
function init(){

    //engine instance
    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    
    //insert canvas
    document.getElementById("container").appendChild(renderer.domElement);

    //instance scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0.5, 0.5, 0.5);

    //camera
    camera = new THREE.PerspectiveCamera(100, window.innerWidth/window.innerHeight, 1, 500 );
    camera.position.set(65,225,100);
    camera.lookAt(0, 125, 0);
}

function loadScene(){
    material = new THREE.MeshBasicMaterial({color: "yellow", wireframe: true});

    //floor
    const floor = new THREE.Mesh( new THREE.PlaneGeometry(1000, 1000, 5, 5), material);

    floor.rotateX(-Math.PI/2); // floor.rotate.x = -Math.PI/2
    scene.add(floor);
    floor.position.y = -0.2;

    //Robot creation
    robot = new THREE.Object3D();

    //1-base
    const base = new THREE.Mesh( new THREE.CylinderGeometry(50, 50, 15, segments, 5), material )
    robot.add(base);

    //2-robot arm
    robot.add(createArm());

    //3-robot forearm
    robot.add(createForeArm())
    
    //4-robot fingers
    const fingers = createBothFingers()
    fingers.position.y = 200;
    robot.add(fingers)

    scene.add(robot);

    scene.add(new THREE.AxesHelper(3));
}

function render(){
    requestAnimationFrame(render);
    renderer.render(scene, camera);
}

function createArm(){
    const arm = new THREE.Object3D();
    const axis = new THREE.Mesh( new THREE.CylinderGeometry(radius, radius, depth, segments/2, 10), material )
    axis.rotateX(-Math.PI/2)
    const armBar = new THREE.Mesh( new THREE.BoxGeometry(12, height, depth), material )
    armBar.position.y = height/2;
    const articulation = new THREE.Mesh( new THREE.SphereGeometry(radius, segments/4, segments/4), material )
    articulation.position.y = height;
    arm.add(axis);
    arm.add(armBar);
    arm.add(articulation);
    return arm;
}

function createForeArm() {

    const foreArm = new THREE.Object3D();
    const base = new THREE.Mesh( new THREE.CylinderGeometry(radius+2, radius+2, 6, 10, 10), material );
    foreArm.add(base);
    for (let index = 0; index < 4; index++) {
        const bar = new THREE.Mesh( new THREE.BoxGeometry(4, 80, 4), material );
        bar.matrixAutoUpdate = false;
        var mt = new THREE.Matrix4();
        var mr = new THREE.Matrix4();
        mt.makeTranslation(11,40,0);
        mr.makeRotationY(index*Math.PI/2);
        bar.matrix = mr.multiply(mt)
        foreArm.add(bar);
    }
    const hand = new THREE.Mesh( new THREE.CylinderGeometry(15,15,40, 10, 10), material )
    hand.rotateX(-Math.PI/2);
    hand.position.y = 80;
    foreArm.add(hand)
    foreArm.position.y = height;
    return foreArm;

}
function createBothFingers(){ 
    const fingers = new THREE.Object3D();
    const finger1 = createFinger()
    finger1.rotateX(-Math.PI/2)
    fingers.add(finger1);

    const finger2 = createFinger()
    finger2.rotateX(-Math.PI/2)
    finger2.position.z = -20
    fingers.add(finger2);

    return fingers;
}

function createFinger(){

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
    -1,0,0, -1,0,0, -1,0,0, -1,0,0,
    
    //big rectangle right X
    1,0,0, 1,0,0, 1,0,0, 1,0,0,

    //polygon top X
    0,1,0, 0,1,0, 0,1,0, 0,1,0,
    
    //polygon front X
    0,0,1, 0,0,1, 0,0,1, 0,0,1,
    
    //polygon bottom X
    2,-19,0, 2,-19,0, 2,-19,0, 2,-19,0,  
    
    //polygon left X
    5,0,19, 5,0,19, 5,0,19, 5,0,19, 
    
    //polygon right X
    -5,0,19, -5,0,19, -5,0,19, -5,0,19
    
]

// 0, -8, -10, //0
// 19, -8, -10, //1
// 0, -8, 10, //2
// 19, -8, 10, //3
// 0, -12, -10, //4
// 19, -12, -10, //5
// 0, -12, 10, //6
// 19, -12, 10, //7
// 38, -8, -5, //8
// 38, -12, -5, //9
// 38, -8, 5, //10
// 38, -12, 5, //11       

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
    console.log(finger)
    finger.setIndex(indexes);
    finger.setAttribute("position", new THREE.Float32BufferAttribute(coords,3));
    finger.setAttribute("normal", new THREE.Float32BufferAttribute(norms,3));
    return new THREE.Mesh(finger, material); 

}
