const video = document.getElementById('video')
const mediaStream = new MediaStream();

navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.oGetUserMedia || navigator.msGetUserMedia;

if (navigator.getUserMedia){
    navigator.getUserMedia({audio:false,video:true},streamWebCam,throwError);
}

function streamWebCam (mediaStream) {
    video.srcObject = mediaStream;
}

function throwError (e) {
    alert(e.name);
}

// function startup() {
//     navigator.mediaDevices.getUserMedia({
//         audio: false,
//         video: {
//             width: { min: 1024, ideal: 1280, max: 1920 },
//             height: { min: 576, ideal: 720, max: 1080 },
//             facingMode: "environment"
//         }
        
//     }).then(stream => {video.srcObject = stream;}).catch(console.error)
// }

// window.addEventListener('load', startup, false);