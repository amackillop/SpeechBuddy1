function googleResponse(data) {
	console.log("Google ran")
    text_title = document.getElementById("header-text");
    text_title.innerHTML = "Your transcript: ";

    transcript = document.getElementById("transcript-display");
    transcript.innerHTML = data.transcript;

    confidence = document.getElementById("confidence");
    confidence.innerHTML = "Confidence: " + data.confidence;
    confidence.style.display = "block";
}