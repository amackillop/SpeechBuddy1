function fillerCountResponse(data) {
    console.log("count ran")
    document.getElementById("count").innerHTML = "<h2>Filler words: " + data.filler_count + "<h2>"

    }