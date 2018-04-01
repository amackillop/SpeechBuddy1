
function googleResponse(data) {

    //handle sliding + loading icon
    $("#myloader").hide();
    loadAnalyticsPage();
    $("#right-split").animate({ width: '100%' }, 1500);
    displayTranscriptWPM(data);
    updateQuickData(data);
    displayGraphs(data);
}

function loadingTranscript() {

    $("#submit-btn").prop('disabled', true);
    $("#header-text").remove();
    $("#text-wrapper").hide();

    $('#right-split').prepend('<div class = "loader" id = "myloader" align="center" hidden = "true"></div>');
    $("#myloader").fadeIn("slow");
}


//this is a variable that contains the entire analytics page. It will be loaded once the google response returns
var analytics_page = `
    <div class="container-fluid">
        <div class="row">  
            <br>

            <div class="col-sm-12">
                <div class="well well-sm " >
                    <div style="text-align:left">
                        <div>
                            <p style="font-size:16px; margin:0px" class="btn" >Record / <b>Transcript Analysis</b></p>
                        </div>
                    </div>                      
                </div>
                <div class="row" style="height: 35vw">
                    <div class="col-sm-6" >
                        <div class="well" style="height: 34vw;overflow-y: scroll">
                            <h2>Here's what you said:</h2>
                            <h4 id ="empty-transcript" style="line-height: 2.4; margin: 40px"></h4>
                        </div>
                    </div>   

                    <div class="col-sm-1">
                        <div class="well well-sm">
                            <h4 style="font-size: 1vw"><b>Score</b></h4>
                            <h4 style="font-size: 1.5vw" class = "med">82.5%</h4>
                        </div>
                    </div>
                    <div class="col-sm-1">
                        <div class="well well-sm">
                            <h4 style="font-size: 1vw"><b>WPM</b></h4>
                            <h4 style="font-size: 1.5vw" class="med">145</h4>
                        </div>
                    </div>
                    <div class="col-sm-1">
                        <div class="well well-sm">
                            <h4 style="font-size: 1vw"><b>Words</b></h4>
                            <h4 style="font-size: 1.5vw"  class="low">323</h4>
                        </div>
                    </div>
                    <div class="col-sm-1">
                        <div class="well well-sm">
                            <h4 style="font-size: 1vw"><b>Fillers</b></h4>
                            <h4 style="font-size: 1.5vw" class="very-high">7</h4>
                        </div>
                    </div>
                    <div class="col-sm-1">
                        <div class="well well-sm">
                            <h4 style="font-size: 1vw"><b>Tone:</b></h4>
                            <h4 style="font-size: 1.5vw" class="low">Neutral</h4>
                        </div>
                    </div>
                    <div class="col-sm-1">
                        <div class="well well-sm">
                            <h4 style="font-size: 1vw"><b>Duration</b></h4>
                            <h4 style="font-size: 1.5vw">2:49s</h4>
                        </div>
                    </div>
                    <div class="col-sm-6">
                        <div class="well">
                            <ul class="nav nav-tabs">
                                <li class="active"><a href="#">Tone</a></li>
                                <li ><a href="#">Volume</a></li>
                                <li><a href="#">Corpus</a></li>
                                <li><a href="#">Emotions</a></li>
                            </ul>
                            <div>
                                <img style="height: 20vw;width:45vw" src="https://www.mathworks.com/matlabcentral/mlc-downloads/downloads/submissions/22214/versions/1/screenshot.jpg">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="well well-sm" style="text-align:left">
                    <audio controls style="width: 95%; margin-top: 0px" src="audio/Simon_Sinek_30.flac"
                        ontimeupdate="document.getElementById('tracktime').innerHTML = 'Track time: ' + Math.floor(this.currentTime) + ' / ' + Math.floor(this.duration);">
                    </audio>
                </div>
                <div class="well well-sm" style="text-align:left">
                <ul class="legend">
                <li><span class="too_slow"></span> Too Slow</li>
                <li><span class="slow"></span> Slow</li>
                <li><span class="good"></span> Good</li>
                <li><span class="fast"></span> Fast</li>
                <li><span class="too_fast"></span> Too Fast</li>
                </ul>
                </div>
            </div>
        </div>
    </div>
    `;

function loadAnalyticsPage() {
    $("#right-split").append(analytics_page);
}

function displayTranscriptWPM(data) {

    var temp1 = document.getElementById("empty-transcript");
    for (i = 0; i < data.wordsperminute.length - 1; i++) {
        if (data.wordsperminute[i] <= 120) {
            var temp3 = document.createElement("div");
            temp3.setAttribute("class", "too_slow");
            var node = document.createTextNode(data.list_of_sentences[i]);
            temp3.appendChild(node);
            temp1.appendChild(temp3);
        }
        else if (data.wordsperminute[i] > 120 && data.wordsperminute[i] <= 140) {
            var temp3 = document.createElement("div");
            temp3.setAttribute("class", "slow");
            var node = document.createTextNode(data.list_of_sentences[i]);
            temp3.appendChild(node);
            temp1.appendChild(temp3);
        }
        else if (data.wordsperminute[i] > 140 && data.wordsperminute[i] <= 170) {
            var temp3 = document.createElement("div");
            temp3.setAttribute("class", "good");
            var node = document.createTextNode(data.list_of_sentences[i]);
            temp3.appendChild(node);
            temp1.appendChild(temp3);
        }
        else if (data.wordsperminute[i] > 170 && data.wordsperminute[i] <= 190) {
            var temp3 = document.createElement("div");
            temp3.setAttribute("class", "fast");
            var node = document.createTextNode(data.list_of_sentences[i]);
            temp3.appendChild(node);
            temp1.appendChild(temp3);
        }
        else if (data.wordsperminute[i] > 190) {
            var temp3 = document.createElement("div");
            temp3.setAttribute("class", "too_fast");
            var node = document.createTextNode(data.list_of_sentences[i]);
            temp3.appendChild(node);
            temp1.appendChild(temp3);
        }
    }
}