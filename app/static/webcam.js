var socket = io.connect('http://localhost:5000');
let v = document.getElementById('myVideo');
var userConsent = document.getElementById('consent')

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
    socket.emit('send image', {'image': file});
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

//Take a picture on click
v.onclick = function() {
    console.log('click');
    sendImagefromCanvas();
};

function record() {
    window.setInterval(function() {
    console.log('interval');
    sendImagefromCanvas();
    }, 10000);
}

//record();
//socket.on('connected')

if (userConsent != null && userConsent.getAttribute('data') == '1') {
    console.log('start recording');
    record();
}




