function googleResponse(data) {
	console.log("Google ran")
    transcript = document.getElementById("transcript");
    transcript.style.display = "block";
    content = document.getElementById("string");
    content.innerHTML=data.transcript;

    
    console.log("hello")

    confidence = document.getElementById("confidence");
    confidence.innerHTML = "Confidence.    " + data.confidence;
    confidence.style.display = "block";
    div = document.getElementById("recordingDiv");
    div.style.display = "none";

}