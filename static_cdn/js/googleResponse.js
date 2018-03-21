function googleResponse(data) {
	console.log("Google ran")
    transcript = document.getElementById("transcript");
    transcript.style.display = "block";
    content = document.getElementById("string");
    content.innerHTML=data.transcript;

    confidence = document.getElementById("confidence");
    confidence.innerHTML = "Confidence.    " + data.confidence;
    confidence.style.display = "block";
    // div = document.getElementById("recordingDiv");
    // div.style.display = "none";


    //once google response arrives, hide the submit button
    var hide_submit = document.getElementById('submit-btn');
    // hide_submit.disabled = "false";
    hide_submit.style.display = "none";

}