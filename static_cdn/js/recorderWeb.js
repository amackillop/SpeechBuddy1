// Expose globally your audio_context, the recorder instance and audio_stream
var audio_context;
var recorder;
var audio_stream;

/**
 * Patch the APIs for every browser that supports them and check
 * if getUserMedia is supported on the browser.
 *
 */
function Initialize() {
	try {
		// Monkeypatch for AudioContext, getUserMedia and URL
		window.AudioContext = window.AudioContext || window.webkitAudioContext;
		navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia;
		window.URL = window.URL || window.webkitURL;

		// Store the instance of AudioContext globally
		audio_context = new AudioContext;

		//hide "submit button" for now
		var submit_btn = document.getElementById("submit-btn");
		submit_btn.style.display = "none";
		console.log('Audio context is ready !');
		console.log('navigator.getUserMedia ' + (navigator.getUserMedia ? 'available.' : 'not present!'));
	} catch (e) {
		alert('No web audio support in this browser!');
	}
}

/**
 * Starts the recording process by requesting the access to the microphone.
 * Then, if granted proceed to initialize the library and store the stream.
 *
 * It only stops when the method stopRecording is triggered.
 */
function startRecording() {
	// Access the Microphone using the navigator.getUserMedia method to obtain a stream
	navigator.getUserMedia({ audio: true }, function (stream) {
		// Expose the stream to be accessible globally
		audio_stream = stream;
		// Create the MediaStreamSource for the Recorder library
		var input = audio_context.createMediaStreamSource(stream);
		console.log('Media stream succesfully created');

		// Initialize the Recorder Library
		recorder = new Recorder(input);
		console.log('Recorder initialised');

		// Start recording !
		recorder && recorder.record();
		console.log('Recording...');

		// Disable Record button and enable stop button !
		document.getElementById("start-btn").disabled = true;
		document.getElementById("stop-btn").disabled = false;
	}, function (e) {
		console.error('No live audio input: ' + e);
	});
}

/**
 * Stops the recording process. The method expects a callback as first
 * argument (function) executed once the AudioBlob is generated and it
 * receives the same Blob as first argument. The second argument is
 * optional and specifies the format to export the blob either wav or mp3
 */
function stopRecording(callback, AudioFormat) {
	// Stop the recorder instance
	recorder && recorder.stop();
	console.log('Stopped recording.');

	// Stop the getUserMedia Audio Stream !
	audio_stream.getAudioTracks()[0].stop();
	console.log(audio_stream.getAudioTracks());

	// Disable Stop button and enable Record button !
	document.getElementById("start-btn").disabled = false;
	document.getElementById("stop-btn").disabled = true;
	// var submit_btn = document.getElementById("submit-btn");
	// submit_btn.style.display = "inline";
	// var gDrive_button = document.getElementById("upload-btn");
	// gDrive_button.style.display = "inline";
	$("#submit-btn").fadeIn( "slow" );
	$("#upload-btn").fadeIn( "slow" );

	// Use the Recorder Library to export the recorder Audio as a .wav file
	// The callback providen in the stop recording method receives the blob
	if (typeof (callback) == "function") {

		/**
		 * Export the AudioBLOB using the exportWAV method.
		 * Note that this method exports too with mp3 if
		 * you provide the second argument of the function
		 */
		recorder && recorder.exportWAV(function (blob) {
			callback(blob);
			console.log(blob);


			$("#submit-btn").click(function () {
				var csrftoken = getCookie('csrftoken');
				console.log(csrftoken);
				// console.log(typeof($('#string').html()));
				var fd = new FormData();
				var reader = new FileReader();
				//console.log(reader.readAsDataURL(AudioBLOB))
				var fileType = 'audio';
				var fileName = 'output.wav';
				fd.append(fileType, blob, fileName);
				// set csrf header
				console.log("Before Ajax");
				console.log(fd)
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
					url: "/api/google/",
					data: fd,
					processData: false,
					contentType: false,
					type: 'POST',
					success: function (data) {
						console.log("SUCCESS");
						googleResponse(data);
						nltkCorpus(data);
						pitchResponse(data);
						volumeResponse(data);
						fillerCountResponse(data);
						//SentenceSpeed(data);
						//console.log(data);
					}
				});
			})
			// create WAV download link using audio data blob
			// createDownloadLink();

			// Clear the Recorder to start again !
			recorder.clear();
		}, (AudioFormat || "audio/wav"));

	}
	//submit_btn.disabled = "false";
}

// Initialize everything once the window loads
window.onload = function () {
	// Prepare and check if requirements are filled
	Initialize();

	// Handle on start recording button
	document.getElementById("start-btn").addEventListener("click", function () {
		startRecording();
	}, false);

	// Handle on stop recording button
	document.getElementById("stop-btn").addEventListener("click", function () {
		// Use wav format
		var _AudioFormat = "audio/wav";
		// You can use mp3 to using the correct mimetype
		//var AudioFormat = "audio/mpeg";

		stopRecording(function (AudioBLOB) {
			// Note:
			// Use the AudioBLOB for whatever you need, to download
			// directly in the browser, to upload to the server, you name it !

			// In this case we are going to add an Audio item to the list so you
			// can play every stored Audio
			var url = URL.createObjectURL(AudioBLOB);
			console.log(url);
			var li = document.createElement('li');
			var au = document.createElement('audio');
			au.setAttribute("class", "record-controls")
			var hf = document.createElement('a');

			au.controls = true;
			au.src = url;
			hf.href = url;
			// Important:
			// Change the format of the file according to the mimetype
			// e.g for audio/wav the extension is .wav
			//     for audio/mpeg (mp3) the extension is .mp3
			hf.download = 'output.wav';
			hf.setAttribute("id", "audioFileUpload");
			hf.innerHTML = hf.download;
			recording_div = document.getElementById("recordingDiv");
			recording_div.appendChild(au);
			//li.appendChild(hf);
			var file = audio_stream.getAudioTracks()[0];
			//fileURL = AudioBLOB.createObjectURL(file);
			//console.log(fileURL);

			// var rlist = document.getElementById("recordingslist");
			// if(rlist.hasChildNodes()){
			//     rlist.removeChild(rlist.firstChild);
			// }
			// recordingslist.appendChild(li);
			//  var x = document.getElementById("recordingtitle");
			//  x.style.display = "block";
		}, _AudioFormat);
	}, false);
};



