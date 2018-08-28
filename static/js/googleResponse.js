
var global_data;
var recorded_video;

function googleResponse(data) {
    console.log(data);
    global_data = data;

    //handle sliding + loading icon
    $("#myloader").hide();
    loadAnalyticsPage();
    $("#right-split").animate({ width: '100%' }, 1500);
    displayTranscript(data)
    displayTranscriptWPM(data);
    displayGraphs(data);
    displayQuickData(data);
    fillerScript(data);
    wpmTranscript();
}

function loadingTranscript() {
    $("#submit-btn").prop('disabled', true);
    $("#header-text").remove();
    $("#text-wrapper").hide();

    $('#right-split').prepend('<div class = "loader" id = "myloader" align="center" hidden = "true"></div>');
    $("#myloader").fadeIn("slow");
}

function displayGraphs(data) {
    var transcript_split = data.transcript.split("\"");
    var corpusTranscript = transcript_split[1];
    $("#corpusTranscript").text(corpusTranscript);
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

                            <p id = "CurrentTime">sfbv</p>
                        </div>
                    </div>                      
                </div>
                <div class="row" style="height: 35vw">
                    <div class="col-sm-6" >
                        <div class="well" style="height: 37vw; padding: 0 ">
                            <div class="well-sm" style="height: 18vw;background-color: black">
                                <video id="videoPlayback" style="height: 17vw; transform: rotateY(180deg);" class="center" muted></video>
                            </div>
                            <div style="overflow-y: scroll; height: 18vw">
                                
                                <ul class="legend" style="margin-top:10px">
                                    <li><span class="legend too_slow"></span> Too Slow</li>
                                    <li><span class="slow"></span> Slow</li>
                                    <li><span class="good"></span> Good</li>
                                    <li><span class="fast"></span> Fast</li>
                                    <li><span class="too_fast"></span> Too Fast</li>
                                </ul>
                          
                                <h4 id ="empty-transcript" style="line-height: 2.4; margin: 40px"></h4>
                                <h4 id = "corpus-Transcript" style="line-height: 2.4; margin: 40px;display:none"></h4>
                                <h4 id ="Audio-transcript" style="line-height: 2.4; margin: 40px;display:none"></h4>
                                <h4 id = "filler-Transcript" style="line-height: 2.4; margin: 40px;display:none"></h4>
                            </div>
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
                            <h4 id="Tone" style="font-size: 1.5vw" class="low">Neutral</h4>
                        </div>
                    </div>
                    <div class="col-sm-1">
                        <div class="well well-sm">
                            <h4 style="font-size: 1vw"><b>Duration</b></h4>
                            <h4 id="track-time" style="font-size: 1.5vw" onload="this.">2:49s</h4>
                        </div>
                    </div>
                    <div class="col-sm-6">
                        <div class="well">
                            <ul class="nav nav-tabs">
                                <li class="active"><a data-toggle="tab" href="#home"  onclick = "wpmTranscript()">Tone</a></li>
                                <li><a data-toggle="tab" href="#menu1"  onclick = "wpmTranscript()">Volume</a></li>
                                <li><a data-toggle="tab" href="#menu2"  onclick = "corpusTranscript()">Corpus</a></li>
                                <li><a data-toggle="tab" href="#menu3"  onclick = "EmotionPieCreate(global_data)">Emotion</a></li>
                                <li><a data-toggle="tab" href="#menu4"  onclick = "AudioTranscript()">Emotion</a></li>
                                <li><a data-toggle="tab" href="#menu5"  onclick = "fillerTranscript()">Filler Content</a></li>
                            </ul>
                            <div class="tab-content">
                                <div id="home" class="tab-pane fade in active">
                                    <div id="chart_div" style="height:20vw;width:42vw">
                                    </div>
                                </div>
                                <div id="menu1" class="tab-pane fade">
                                    <canvas id="VolumeLineChart" width="42vw" height="20vw"></canvas>
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
                                <div id="menu4" class="tab-pane fade">
                                    <canvas id="EmotionTextBarChart" width="42vw" height="20vw"></canvas>
                                </div>
                                <div id="menu5" class="tab-pane fade">
                                    <div id="fillerDiv" width="42vw" height="20vw">

                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class= "row">
            <div class="well well-sm" style="text-align:left; margin:15px;  margin-top:5px">
                <audio id="audioplayer" controls style="width: 100%; margin-top: 0px" src="audio/output_mono.flac"
                ontimeupdate="changeTimes(Math.floor(this.currentTime), global_data.sentencesEnd);">
                </audio>
            </div>
        </div>
    </div>
    `;

function loadAnalyticsPage() {
    $("#right-split").append(analytics_page);
    var audio_playback = document.getElementById("audioplayer");
    var video_playback = document.getElementById("videoPlayback");
    var recorded_video = document.getElementById("videoElement");
    
    console.log("rec_vid url:" + recorded_video.src);

    video_playback.src = recorded_video.src;

    console.log("video_play url:" + video_playback.src);
    
    audio_playback.onplay = function(){
        video_playback.play();
    }    
}

var counter = 0;

function changeTimes(info, sentencesEnd){
     if (!$("#Audio-transcript").is(":visible")) {
        AudioTranscript();
        for (i = 0; i < document.getElementById('Audio-transcript').childNodes.length; i++) {
            document.getElementById('Audio-transcript').childNodes[i].className = "basic_transcript";
         }
     }
    document.getElementById('CurrentTime').innerHTML = info;

    if(info == 0){
    //    console.log(document.getElementById('empty-transcript').childNodes[0]);
        document.getElementById('Audio-transcript').childNodes[0].className = "reading_transcript";
    }
    // console.log(info, sentencesEnd, counter);
    if(info + 1 > sentencesEnd[counter]){
        document.getElementById('Audio-transcript').childNodes[counter].className = "basic_transcript";
        counter = counter + 1;
        document.getElementById('Audio-transcript').childNodes[counter].className = "reading_transcript";
    }
}

function displayTranscript(data){
    var mainTranscript = document.getElementById("Audio-transcript");
    for (i = 0; i < data.wordsperminute.length; i++) {
        var sentenceDiv = document.createElement("div");
        sentenceDiv.setAttribute("class", "basic_transcript");
        var node = document.createTextNode(data.list_of_sentences[i]);
        sentenceDiv.appendChild(node);
        mainTranscript.appendChild(sentenceDiv);
    }

}


function displayQuickData(data) {
    //set confidence level
    $("#score-data").text(data.confidence);
    $("#WPM").text(data.average_wpm);
    $("#Words").text(data.total_words);
    $("#filler-count-val").text(data.fillerCount);
    ToneMethod(data)
    //set track duration
    // var track_time = Math.floor($("#audioplayer").duration);
    // $("#track-time").text(track_time);
}

function corpusTranscript() {
    if (!$("#corpus-Transcript").is(":visible")) {
        $("#empty-transcript").hide();
        $("#Audio-transcript").hide();
        $("#filler-Transcript").hide();
        $("#corpus-Transcript").show();
    }
}

function wpmTranscript() {
    if (!$("#empty-transcript").is(":visible")) {
        $("#corpus-Transcript").hide();
        $("#Audio-transcript").hide();
        $("#filler-Transcript").hide();
        $("#empty-transcript").show();
    }
}

function fillerTranscript() {
    if (!$("#filler-Transcript").is(":visible")) {
        $("#corpus-Transcript").hide();
        $("#Audio-transcript").hide();
        $("#empty-transcript").hide();
        $("#filler-Transcript").show();
    }
}

function AudioTranscript() {
    if (!$("#Audio-transcript").is(":visible")) {
        for (i = 0; i < document.getElementById('Audio-transcript').childNodes.length; i++) {
            document.getElementById('Audio-transcript').childNodes[i].className = "basic_transcript";
     }
        $("#filler-Transcript").hide();
        $("#empty-transcript").hide();
        $("#corpus-Transcript").hide();
        $("#Audio-transcript").show();

    }
}

function ToneMethod(data){
    console.log('Tone Method Testing')
    console.log(data.AvgT, document.getElementById("Tone").innerHTML);
    var tonetemp=Math.max.apply(Math, data.AvgT);
    console.log(tonetemp);
    for (i = 0; i < data.AvgT.length; i++) {
        if(data.AvgT[i]==tonetemp){
            console.log(i,data.AvgT[i])
            if(i == 0){
                $("#Tone").text("Sadness");
            }
            else if(i == 1){
                $("#Tone").text("Joy");

            }
            else if(i == 2){
                $("#Tone").text("Anger");

            }
            else if(i == 3){
                $("#Tone").text("Disgust");

            }
            else if(i == 4){
                $("#Tone").text("Fear");

            }
        }
    }

}

function fillerScript(data){
    fillerTranscript();

    var res = (data.filler)

    var x = document.createElement("table");
    x.setAttribute("id", "myTableFiller");
    x.setAttribute("class", "table");
    var tb = document.createElement("tbody");
    tb.setAttribute("id", "tbodyFiller")
    var y, t, z;
    var index = 0;
    keys = Object.keys(res);
    console.log(keys)
    for (row = 0; row < 3; row++) {
        y = document.createElement("TR");
        y.setAttribute("id", "rowF" + row);
        for (col = 0; col < 3; col++) {
            z = document.createElement("TD");
            z.setAttribute("idF", "child" + index);
            z.setAttribute("class", "result");
            var t = document.createTextNode(keys[index] + ":  " + res[keys[index]]);
            index = index + 1;
            z.appendChild(t);
            y.appendChild(z);
        }
        tb.appendChild(y);
    }

    x.appendChild(tb);

    $("#fillerDiv").prepend(x);

    tempString = ""
    for (i = 1; i < data.tok.length; i++) {
        tempString = tempString + " " + data.tok[i];
    }
    $('#filler-Transcript').html(tempString);

    $(document).on(
        {
            mouseenter: function () {
                var word = $(this).text()
                word = word.slice(0, word.indexOf(":"));
                indices = data.indexArray;
                indices = JSON.parse(indices);
                tempString = "";
                // console.log(word);
                for (i = 1; i < data.tok.length; i++) {
                    if(i==39){
                        // console.log(i,data.tok[i], word, word == String(data.tok[i]),typeof(word),typeof(data.tok[i]));

                    }
                    if (word == String(data.tok[i])) {
                        tempString = tempString + " <mark class = 'too_fast'> " + data.tok[i] + " </mark> ";
                    }
                    else {
                        tempString = tempString + " " + data.tok[i];
                    }
                }
                // console.log(tempString);
                document.getElementById('filler-Transcript').innerHTML = tempString;
            },
            mouseleave: function () {
                $(this).css("background", "white");
                // $("#results").children().css("opacity", 1);
            }

        }, ".result");


}



