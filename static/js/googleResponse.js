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

    
    list_of_sentences = document.getElementById("list_of_sentences");
    //list_of_sentences.innerHTML = data.list_of_sentences[0];

    wordsperminute = document.getElementById("wordsperminute")
    //wordsperminute.innerHTML = data.wordsperminute[0]
    //console.log(data.wordsperminute.length);
    console.log(data.list_of_sentences.length);

    var temp1 = document.getElementById("Empty Transcript");
    for(i = 0; i < data.wordsperminute.length+1 ; i++){
        if(data.wordsperminute[i]<=120){
            var temp3 = document.createElement("div"); 
            temp3.setAttribute("class","too_slow");
            // temp3.setAttribute("id","sen" + i);
            var node = document.createTextNode(data.list_of_sentences[i]);
            temp3.appendChild(node);
            // $(temp3).append(node);
            // $(temp1).append(temp3);
            temp1.appendChild(temp3);
        }
         else if(data.wordsperminute[i] > 120 && data.wordsperminute[i]<= 140){
            var temp3 = document.createElement("div"); 
            temp3.setAttribute("class","slow");
            // temp3.setAttribute("id","sen" + i);
            var node = document.createTextNode(data.list_of_sentences[i]);
            temp3.appendChild(node);
            // $(temp3).append(node);
            // $(temp1).append(temp3);
            temp1.appendChild(temp3);

         }
        else if(data.wordsperminute[i] > 140 && data.wordsperminute[i] <= 170){
            var temp3 = document.createElement("div"); 
            temp3.setAttribute("class","good");
            // temp3.setAttribute("id","sen" + i);
            var node = document.createTextNode(data.list_of_sentences[i]);
            temp3.appendChild(node);
            // $(temp3).append(node);
            // $(temp1).append(temp3);
            temp1.appendChild(temp3);
 }
         else if(data.wordsperminute[i] > 170 && data.wordsperminute[i] <= 190){
            var temp3 = document.createElement("div"); 
            temp3.setAttribute("class","fast");
            // temp3.setAttribute("id","sen" + i);
            var node = document.createTextNode(data.list_of_sentences[i]);
            temp3.appendChild(node);
            // $(temp3).append(node);
            // $(temp1).append(temp3);
            temp1.appendChild(temp3);
        }
         else if(data.wordsperminute[i] > 190){
            var temp3 = document.createElement("div"); 
            temp3.setAttribute("class","too_fast");
            // temp3.setAttribute("id","sen" + i);
            var node = document.createTextNode(data.list_of_sentences[i]);
            temp3.appendChild(node);
            // $(temp3).append(node);
            // $(temp1).append(temp3);
            temp1.appendChild(temp3);
        }
     }
}

function loadingTranscript(){
    
    $("#submit-btn").prop('disabled', true);
    $("#header-text").remove();
    $("#text-wrapper").hide();

    $('#right-split').prepend('<div class = "loader" id = "myloader" align="center" hidden = "true"></div>');
    $("#myloader").fadeIn( "slow" );

    
    //$("#transcript-display").hide();
}

// function SentenceSpeed(data){
//     //console.log("Testingtesting");
//     //console.log(string(data.wordsperminute[0]));
//     for(i = 0; i < data.wordsperminute.length ; i++){
//         console.log(data.wordsperminute.length);
//         if(data.wordsperminute[i]<=120){
//             var temp=data.list_of_sentences[i];
//             var temp2=document.getElementById("Empty Transcript").textContent;
//             document.getElementById("Empty Transcript").textContent=temp2 + temp
//             console.log("Temp is nOOOOOt");
//         }
//          else if(data.wordsperminute[i] > 120 && data.wordsperminute[i]<= 140){
//             var temp=data.list_of_sentences[i];
//             var temp2=document.getElementById("Empty Transcript").textContent;
//             document.getElementById("Empty Transcript").textContent=temp2 + temp
//             console.log("Temp is nOOOOOt2");

//          }
//         else if(data.wordsperminute[i] > 140 && data.wordsperminute[i] <= 170){
//             var temp=data.list_of_sentences[i];
//             var temp2=document.getElementById("Empty Transcript").textContent;
//             document.getElementById("Empty Transcript").textContent=temp2 + temp
//             console.log("Temp is nOOOOOt3");

//  }
//          else if(data.wordsperminute[i] > 170 && data.wordsperminute[i] <= 190){
//             var temp=data.list_of_sentences[i];
//             var temp2=document.getElementById("Empty Transcript").textContent;
//             document.getElementById("Empty Transcript").textContent=temp2 + temp
//             console.log("Temp is nOOOOOt4");

//         }
//          else if(data.wordsperminute[i] > 190){
//             var temp=data.list_of_sentences[i];
//             var temp2=document.getElementById("Empty Transcript").textContent;
//             document.getElementById("Empty Transcript").textContent=temp2 + temp
//             console.log("Temp is nOOOOOt5");

//         }

//      }}
