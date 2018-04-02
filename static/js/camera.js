// var scr_shot = setInterval(oneSecondFunction, 1000);

//START VIDEO STREAMING
var video = document.querySelector("#videoElement");

// The getUserMedia interface is used for handling camera input.
// Some browsers need a prefix so here we're covering all the options       
navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia || navigator.oGetUserMedia;

if (navigator.getUserMedia) {
    navigator.getUserMedia({ video: true }, handleVideo, videoError);
}

function handleVideo(stream) {
    video.src = window.URL.createObjectURL(stream);
}

function videoError(e) {
    // do something
}
//END VIDEO STREAMING


function oneSecondFunction() {
    // var video = document.querySelector("#videoElement");
    const button = document.querySelector('#start-btn');
    const img = document.querySelector('#screenshot-img');
    // const video = document.querySelector('#screenshot-video');
    const canvas = document.createElement('canvas');
    
    button.onclick = video.onclick = function () {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);
        // Other browsers will fall back to image/png
        img.src = canvas.toDataURL('image/png');
    }
    // img.src=img.src.replace('/^data:image\/(png|jpg);base64,/',"");
    // img.href = document.getElementById('canvas').toDataURL();
    // img.download = 'test.png';
    

    var blob = new Blob([img.src], { type: 'image/png' });
    console.log("blob from start button:");
    console.log(blob);

    // downloadCanvas(this, 'canvas', 'test.png');

    function handleSuccess(stream) {
        video.srcObject = stream;
    }
    ImageSaved(blob);
    // navigator.mediaDevices.getUserMedia(constraints).
    //     then(handleSuccess).catch(handleError);

}
//The clearInterval() method clears a timer set with the setInterval() method.
function StopScrnShot() {
    clearInterval(scr_shot);
    var imf = new FormData();
    var reader = new FileReader;
    var fileType = 'image';
    var fileName = 'img.png';
    imf.append(fileType, fileName);

}
function ImageSaved(blob) {

    var csrftoken = getCookie('csrftoken');
    console.log(csrftoken);
    // console.log(typeof($('#string').html()));
    var fd = new FormData();
    var reader = new FileReader();
    //console.log(reader.readAsDataURL(AudioBLOB))
    var fileType = 'image';
    var fileName = 'img.png';
    fd.append(fileType, blob, fileName);
    // set csrf header
    console.log("file from img blob");
    console.log(fd);
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    //while processing the api call, disable the submit button
    //document.getElementById("submit-btn").disabled = "true";
    // Ajax call here
    $.ajax({
        url: "/api/screenshot/",
        data: fd,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function (data) {
            console.log("Image Saved");
        }
    });

}

// function downloadCanvas(link, canvasId, filename) {
//     link.href = document.getElementById(canvasId).toDataURL();
//     link.download = filename;
// }

// document.getElementById('download').addEventListener('click', function() {
//     downloadCanvas(this, 'canvas', 'test.png');
// }, false);