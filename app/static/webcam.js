var socket = io.connect('http://localhost:5000');
let v = document.getElementById('myVideo');
var userConsent = document.getElementById('consent')
var userID = document.getElementById('userid')
//var recordButton = document.getElementById('recordButton')

//create a canvas to grab an image for upload
let imageCanvas = document.createElement('canvas');
let imageCtx = imageCanvas.getContext('2d');

//Add file blob to a form and post
function postFile(file) {
    let formdata = new FormData();
    formdata.append('image', file);
    let xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://localhost:5000/image', true);
    xhr.onload = function () {
        if (this.status === 200)
            console.log(this.response);
        else
            console.error(xhr);
    };
    xhr.send(formdata);
    
}

function postFile2(file) {
    //let formdata = new FormData();
    //formdata.append('image', file);
    var sendData = {'image': file}
    if (userID != null) {
        sendData = {'image': file, 'userid': userID.getAttribute('data')}  
    }
    socket.emit('send image', sendData);
    console.log('sent image');
    /*
    let xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://localhost:5000/image', true);
    xhr.onload = function () {
        if (this.status === 200)
            console.log(this.response);
        else
            console.error(xhr);
    };
    xhr.send(formdata);
    */
}

//Get the image from the canvas
function sendImagefromCanvas() {

    //Make sure the canvas is set to the current video size
    imageCanvas.width = v.videoWidth;
    imageCanvas.height = v.videoHeight;

    imageCtx.drawImage(v, 0, 0, v.videoWidth, v.videoHeight);

    //Convert the canvas to blob and post the file
    imageCanvas.toBlob(postFile2, 'image/jpeg');
}

/*
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
*/



function record() {
    console.log('connected')
    
    if (userConsent != null && userConsent.getAttribute('data') == '1') {
        console.log('start recording');
        //Get camera video
        navigator.mediaDevices.getUserMedia({video: {width: 1280, height: 720}, audio: false})
        .then(stream => {
            v.srcObject = stream;
        })
        .catch(err => {
            console.log('navigator.getUserMedia error: ', err)
        });
        v.style.display = 'inline';
        //recordButton.style.display = 'block';
        window.setInterval(function() {
            console.log('interval');
            sendImagefromCanvas();
            }, 200000);
        };
}
    

socket.on('connect', record);






