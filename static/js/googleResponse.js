function googleResponse(data) {
	console.log("Google ran")
    transcript = document.getElementById("transcript");
    transcript.style.display = "block";
    content = document.getElementById("string");
    content.innerHTML=data.transcript;

    confidence = document.getElementById("confidence");
    confidence.innerHTML = "Confidence.    " + data.confidence;
    confidence.style.display = "block";
}