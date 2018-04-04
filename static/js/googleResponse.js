
var global_data;

function googleResponse(data) {
    console.log(data);
    global_data = data;

    //handle sliding + loading icon
    $("#myloader").hide();
    loadAnalyticsPage();
    $("#right-split").animate({ width: '100%' }, 1500);
    displayTranscriptWPM(data);
    displayGraphs(data);
    displayQuickData(data);
    EmotionTabCreate(data);
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
                        <div id = "left-split" class="well" style="height: 34vw;overflow-y: scroll">
                            <h2>Here's what you said:</h2>
                            <h4 id ="empty-transcript" style="line-height: 2.4; margin: 40px"></h4>
                            <h4 id = "corpusTranscript" style="line-height: 2.4; margin: 40px;display:none"></h4>
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
                            <h4 id="WPM" style="font-size: 1.5vw" class = "med"></h4>
                        </div>
                    </div>
                    <div class="col-sm-1">
                        <div class="well well-sm">
                            <h4 style="font-size: 1vw"><b>Words</b></h4>
                            <h4 id="Words" style="font-size: 1.5vw" class = "med"></h4>
                        </div>
                    </div>
                    <div class="col-sm-1">
                        <div class="well well-sm">
                            <h4 style="font-size: 1vw"><b>Fillers</b></h4>
                            <h4 id= "filler-count-val" style="font-size: 1.5vw" class="very-high"></h4>
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
                            <ul class="nav nav-tabs">
                                <li class="active"><a data-toggle="tab" href="#home"  onclick = "wpmTranscript()">Tone</a></li>
                                <li><a data-toggle="tab" href="#menu1"  onclick = "wpmTranscript()">Volume</a></li>
                                <li><a data-toggle="tab" href="#menu2"  onclick = "corpusTranscript()">Corpus</a></li>
                                <li><a data-toggle="tab" href="#menu3"  onclick = "wpmTranscript()">Emotion</a></li>
                            </ul>

                            <div class="tab-content">
                                <div id="home" class="tab-pane fade in active">
                                    <div id="chart_div" style="height:20vw;width:42vw">
                                    </div>
                                </div>
                                <div id="menu1" class="tab-pane fade">
                                    <canvas id="VolumeLineChart" width="42vw" height="20vw"></canvas>
                                    </div>
                                </div>
                                <div id="menu2" class="tab-pane fade">
                                    <div id = "data-wrapper">
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
                                </div>
                                <div id="menu3" class="tab-pane fade">
                                    <canvas id="EmotionTextPieChart" width="42vw" height="20vw"></canvas>
                                </div>
                            </div>
                        </div>
                    </div>
                    </div>
                </div>               
            </div>            
        </div>
        <div class="well well-sm" style="text-align:left; margin:10px">
            <ul class="legend">
                <li><span class="legend too_slow"></span> Too Slow(WPM ≤120)</li>
                <li><span class="slow"></span> Slow(>120 WPM ≤140)</li>
                <li><span class="good"></span> Good(>140 WPM ≤170)</li>
                <li><span class="fast"></span> Fast(>170 WPM ≤190)</li>
                <li><span class="too_fast"></span> Too Fast(WPM >190)</li>
            </ul>
        </div>
        <div class="well well-sm" style="text-align:left; margin:10px">
            <audio id="audioplayer" controls style="width: 100%; margin-top: 0px" src="audio/Simon_Sinek_30.flac"
                ontimeupdate="document.getElementById('track-time').innerHTML = Math.floor(this.duration);">
            </audio>
        </div>
    `;

function loadAnalyticsPage() {
    $("#right-split").append(analytics_page);
}

function displayTranscriptWPM(data) {
    var temp1 = document.getElementById("empty-transcript");
    for (i = 0; i < data.wordsperminute.length + 1; i++) {
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
    var transcript_split = data.transcript.split("\"");
    var corpusTranscript = transcript_split[1];
    $("#corpusTranscript").text(corpusTranscript);
}

function displayQuickData(data) {
    //set confidence level
    $("#score-data").text(data.confidence);
    $("#WPM").text(data.average_wpm);
    $("#Words").text(data.total_words);
    $("#filler-count-val").text(data.fillerCount);
    //set track duration
    // var track_time = Math.floor($("#audioplayer").duration);
    // $("#track-time").text(track_time);
}

function corpusTranscript(data) {
    if (!$("#corpusTranscript").is(":visible")) {
        $("#empty-transcript").hide();
        $("#corpusTranscript").show();
    }
}

function wpmTranscript() {
    if ($("#corpusTranscript").is(":visible")) {
        $("#corpusTranscript").hide();
        $("#empty-transcript").show();
    }
}
