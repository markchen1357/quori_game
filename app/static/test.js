var socket = io.connect('http://localhost:5000');
let v = document.getElementById('testVideo');
var userConsent = document.getElementById('consent')
var userID = document.getElementById('userid')
var recordButton = document.getElementById('recordButton')
var startButton = document.getElementById('startButton')

//create a canvas to grab an image for upload
let imageCanvas = document.createElement('canvas');
let imageCtx = imageCanvas.getContext('2d');


function partialApply(fn, ...args) {
    return fn.bind(null, ...args);
}

//Add file blob to a form and post

function emitFile(num, file) {
    //let formdata = new FormData();
    //formdata.append('image', file);
    var sendData = {'image': file}
    if (userID != null) {
        sendData = {'image': file, 'userid': userID.getAttribute('data'), 'num': num}  
    }
    socket.emit('send test', sendData);
    console.log('sent test');
}


//Get the image from the canvas
function sendImagefromCanvas(num) {

    //Make sure the canvas is set to the current video size
    imageCanvas.width = v.videoWidth;
    imageCanvas.height = v.videoHeight;

    imageCtx.drawImage(v, 0, 0, v.videoWidth, v.videoHeight);

    //Convert the canvas to blob and emit the file
    imageCanvas.toBlob(partialApply(emitFile, num), 'image/jpeg');
}

window.onload = function () {

    //Get camera video
    navigator.mediaDevices.getUserMedia({video: {width: 1280, height: 720}, audio: false})
        .then(stream => {
            v.srcObject = stream;
        })
        .catch(err => {
            console.log('navigator.getUserMedia error: ', err)
        });

}


async function test() {
    startButton.setAttribute('disabled', '');
    console.log('starting test');
    socket.emit('start test', {'userid': userID.getAttribute('data')});
    /*
    if (userConsent != null && userConsent.getAttribute('data') == '1') {
        setIntervalX(sendImagefromCanvas, 1000, 10);
    }
    */
    for (i = 0; i < 10; i++) {
        sendImagefromCanvas(i);
        await new Promise(r => setTimeout(r, 1000));
    }
    console.log('finished test');    
}

function passed() {
    console.log('passed test');
    startButton.removeAttribute('disabled');
    window.location.href = 'http://127.0.0.1:5000/training'
}

function failed() {
    console.log('failed test');
    alert('failed test')
    startButton.removeAttribute('disabled');
}


socket.on('failed test', failed)

socket.on('passed test', passed)
    
startButton.onclick = test;

socket.on('connect', function(){startButton.removeAttribute('disabled')});






