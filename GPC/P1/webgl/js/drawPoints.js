/* 
    seminar number one, draw points with VBOs
*/

//vertex shader
const V_SHADER_SOURCE = `
    attribute vec3 pointPosition;
    void main(){
        gl_Position = vec4(pointPosition,1.0);
        gl_PointSize = 10.0;
    }
`
//fragment shader
const F_SHADER_SOURCE = `
    uniform highp vec3 color;
    void main(){
        gl_FragColor = vec4(color, 1.0); //RGBA
    }
`
const cliscs = [];
let fragmentColor;

function main(){
    //retrieve canvas
    const canvas = document.getElementById('canvas');
    const gl = getWebGLContext(canvas)

    //load shaders into the program
    if(!initShaders(gl, V_SHADER_SOURCE, F_SHADER_SOURCE)){
        console.error("error loading shaders");
    }

    //canvas eraser color
    gl.clearColor(0.0,0.0,0.3,1.0)

    //locate position parameter in shader
    const coord = gl.getAttribLocation(gl.program, 'pointPosition');

    //create buffer and stuff
    const bufferVertex = gl.createBuffer();
}