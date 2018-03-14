function googleResponse(data) {
	console.log("google ran")
    transcript = document.getElementById("transcript");
    transcript.style.display = "block";
    content = document.getElementById("string");
    //content.innerHTML = "\"" + (data.transcript).substr(2,data.transcript.length-3) + "\"";
    content.innerHTML=data.transcript;
    confidence = document.getElementById("confidence");

    confidence.innerHTML = "Confidence.    " + data.confidence;
    confidence.style.display = "block";
    div = document.getElementById("recordingDiv");
    div.style.display = "none";

}