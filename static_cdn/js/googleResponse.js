
function googleResponse(data) {

    //handle sliding + loading icon
    $("#myloader").hide();
    loadAnalyticsPage();
    $("#right-split").animate({ width: '100%' }, 1500);
    displayTranscriptWPM(data);
<<<<<<< HEAD
    displayGraphs(data);
    displayQuickData(data);
=======
    updateQuickData(data);
    displayGraphs(data);
>>>>>>> 7b3a95439da1bcc5c041f55c51e5948120e62b0d
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
                            <h4 id="score-data" style="font-size: 1.5vw" class = "med">82.5%</h4>
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
                            <h4 id="track-time" style="font-size: 1.5vw">2:49s</h4>
                        </div>
                    </div>
                    <div class="col-sm-6">
                        <div class="well">
                            <ul class="nav nav-tabs" id="myTab" role="tablist">
                            <li class="nav-item">
                                <a class="nav-link active" id="home-tab" data-toggle="tab" href="#home" role="tab" aria-controls="home" aria-selected="true">Tone</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" id="profile-tab" data-toggle="tab" href="#profile" role="tab" aria-controls="profile" aria-selected="false">Volume</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" id="contact-tab" data-toggle="tab" href="#contact" role="tab" aria-controls="contact" aria-selected="false">Corpus</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" id="emotions-tab" data-toggle="tab" href="#emotions" role="tab" aria-controls="emotions" aria-selected="false">Emotions</a>
                            </li>
                        </ul>
                        <div class="tab-content" id="myTabContent">
                            <div class="tab-pane show active fade in" id="home" role="tabpanel" aria-labelledby="home-tab">
                                <img style="height: 20vw;width:45vw" src="https://www.mathworks.com/matlabcentral/mlc-downloads/downloads/submissions/22214/versions/1/screenshot.jpg">
                            </div>
                            <div class="tab-pane fade" id="profile" role="tabpanel" aria-labelledby="profile-tab">
                                { Volume graph goes here }
                            </div>
                            <div class="tab-pane fade" id="contact" role="tabpanel" aria-labelledby="contact-tab">
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
                            </div>
                            <div class="tab-pane fade" id="emotions" role="tabpanel" aria-labelledby="emotions-tab">
                                { Emotion data goes here }
                            </div>
                        </div>
                    </div>
                    </div>
                </div>
                <div id="random"></div>
                <div class="well well-sm" style="text-align:left">
                    <audio id="audioplayer" controls style="width: 100%; margin-top: 0px" src="audio/Simon_Sinek_30.flac"
                        onload="document.getElementById('track-time').innerHTML = Math.floor(this.duration);">
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

function displayGraphs(data) {
    console.log("Displaying graphs...");
    var all_data = `
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
            
            <div id="chart_div">
            </div>
            
            <div id="volume">
                <div id="chart_div_volume">
                </div>
            </div>
            
            <div id="filler count">
                <div id="count">
                </div>
            </div>
            
        </div>
    </div>
    `;


    var frequencyGraph = `
        <div id="chart_div">
        </div>
    `;

    var volumeGraph = `
        <div id="volume">
            <div id="chart_div_volume">
            </div>
        </div>
    `;

    var fillerData = `
        <div id="filler count">
            <div id="count">
            </div>
        </div>
    `;

    var corpus = `
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
    `;

    $("#freq-graph").append(corpus);
}

function displayQuickData(data) {
    //set confidence level
    $("#score-data").text(data.confidence);

    //set track duration
    // var track_time = Math.floor($("#audioplayer").duration);
    // $("#track-time").text(track_time);
}