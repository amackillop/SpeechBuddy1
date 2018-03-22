function googleResponse(data) {
    console.log("Google ran");

    //handle sliding + loading icon
    $("#myloader").hide();
    $("#text-wrapper").show();
    $("#right-split").animate({width:'100%'}, 1500);
    $("#string").animate({width:'45%'}, 1000);
   
    $("#title").text("Here's what you said:");
    $("#title").fadeIn( "fast" );

    $("#transcript-display").text(data.transcript);
    $("#transcript-display").fadeIn( "slow" );
   
    $('#right-split').prepend('<div class = "split right" id = "data-view"></div>');
    var vol_n_pitch = `
         <div id="myModal" class="modal">
            <div class="modal-content">
                <div class="modal-header">
                    <span class="close">&times;</span>
                    <h2 id="mhead">Modal Header</h2>
                </div>
                <div class="modal-body" id="mbody"></div>
                <div class="modal-footer">
                    <h3>nltk lib</h3>
                </div>
            </div>
        </div>
        <div id = "data-wrapper">
            <div id="fundementals">
                <h2></h2>
                <div id="chart_div" /div>
                </div>
                <div id="volume">
                    <h2></h2>
                    <div id="chart_div_volume" /div>
                    </div>
        
                <div id="filler count">
                    <div id="count">
        
                    </div>
                </div>
            </div>
        </div>
    `;

    $("#data-view").append(vol_n_pitch);

    confidence = document.getElementById("confidence");
    confidence.innerHTML = "Confidence: " + data.confidence;
    confidence.style.display = "block";

}

function loadingTranscript(){
    
    $("#submit-btn").prop('disabled', true);
    $("#header-text").remove();
    $("#text-wrapper").hide();

    $('#right-split').prepend('<div class = "loader" id = "myloader" align="center" hidden = "true"></div>');
    $("#myloader").fadeIn( "slow" );

    
    //$("#transcript-display").hide();
    

}
