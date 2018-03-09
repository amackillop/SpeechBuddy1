jQuery.loadScript = function (url, callback) {
        jQuery.ajax({
        url: url,
        dataType: 'script',
        success: callback,
        async: true
    });
}

function jsUcfirst(string)
{
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function hover(id, data){
            //console.log(data);
            var word = $(this).attr("id")
            console.log(word);
            console.log($(this));
            word = word.slice(1,word.indexOf(":")-1);

            indices = data.indexArray;
            indices = JSON.parse(indices);
            //console.log(indices[word]);
            tempString ="";
            for(i=0; i<data.tok.length; i++){
                //console.log(word)
                if(word == data.tok[i]){
                    tempString = tempString + " <mark>"+ data.tok[i] +"</mark> ";

                }
                else{
                    tempString = tempString + " "+ data.tok[i];

                }
            }
            $('#string').html(tempString);
            //console.log(tempString);
        }

 function nltkCorpus(data){
        str = data.corpus;
        //console.log(data)
        var res = str.split("), (");
        for (i = 0; i < res.length; i++) {
            res[i] = res[i].replace("(","");
            res[i] = res[i].replace(")","");
            res[i] = res[i].replace("[","");
            res[i] = res[i].replace("]","");
            res[i] = res[i].replace(",",":           ");
        }
        //console.log(res);

        var x = document.createElement("table");
        x.setAttribute("id", "myTable");
        x.setAttribute("class", "table");
        var tb = document.createElement("tbody");
        tb.setAttribute("id","tbody")
        var y,t,z;
        var index = 0;
        for (row = 0; row < 4; row++) {
            y = document.createElement("TR");
            y.setAttribute("id", "row"+row);
            for (col = 0; col < 4; col++) {
                z = document.createElement("TD");
                z.setAttribute("id", "child"+index);
                z.setAttribute("class", "result");
                //z.setAttribute("onmouseover", 'hover("child'+index+'", data)');


                var t = document.createTextNode(res[index]);
                index = index + 1;
                z.appendChild(t);
                y.appendChild(z);
                }
            tb.appendChild(y);
        }
        x.appendChild(tb)
        document.body.appendChild(x);

        $(document).on(
  {
    mouseenter: function() {
            var word = $(this).text()
            //console.log(word);
            //console.log($(this));
            word = word.slice(1,word.indexOf(":")-1);

            indices = data.indexArray;
            indices = JSON.parse(indices);
            //console.log(indices[word]);
            tempString ="";
            for(i=0; i<data.tok.length; i++){
                //console.log(word)
                if(word == data.tok[i]){
                    tempString = tempString + " <mark>"+ data.tok[i] +"</mark> ";

                }
                else{
                    tempString = tempString + " "+ data.tok[i];

                }
            }
            $('#string').html(tempString);
    },
    mouseleave: function() {
      $(this).css("background", "white");
      $("#results").children().css("opacity", 1);
    },
    click: function(){
            var modal = document.getElementById('myModal');
            // Get the <span> element that closes the modal
            var btn = $(this);
            var span = document.getElementsByClassName("close")[0];
            var word = $(this).text();
            word = word.slice(1,word.indexOf(":")-1);
            $('#mhead').html(word);            // When the user clicks the button, open the modal
            //btn.onclick = function() {
                modal.style.display = "block";
                syns = JSON.parse(data.listSyn);
                syns = syns = syns[word];
                var keys = Object.keys(syns);
                console.log(syns[keys[0]])
                var lenExamples;
                var mbody = document.getElementById("mbody");
                for(i=0;i < keys.length; i++){
                    z = document.createElement('p')
                    t = document.createTextNode((i+1) + ". "+jsUcfirst(keys[i])+":");
                    z.appendChild(t);
                    mbody.appendChild(z);

                    z = document.createElement('p')
                    t = document.createTextNode("Definition:    " + syns[keys[i]][0]);
                    z.appendChild(t);
                    z.setAttribute("class", "indent");
                    mbody.appendChild(z);

                    lenExamples = syns[keys[i]][1].length
                    console.log(lenExamples);
                    if(typeof(syns[keys[i]][1]) == "string"){
                        lenExamples =1;
                        t = document.createTextNode("Examples:    " + syns[keys[i]][1]);
                        z.appendChild(t);
                        z.setAttribute("class", "indent");
                    }
                    else{
                        for(tempIndex=0;tempIndex<lenExamples;tempIndex++){
                        z = document.createElement('p')
                        if(tempIndex == 0){
                            t = document.createTextNode("Examples:    " + syns[keys[i]][1][tempIndex]);
                            z.appendChild(t);
                            z.setAttribute("class", "indent");
                        }
                        else{
                            t = document.createTextNode(syns[keys[i]][1][tempIndex]);
                            z.appendChild(t);
                            z.setAttribute("class", "indentEX");

                        }
                        mbody.appendChild(z);
                    }
                    }
                    console.log(syns[keys[i]][1])

                }
            //}
            // When the user clicks on <span> (x), close the modal
            span.onclick = function() {
                modal.style.display = "none";
                var myNode = document.getElementById("mbody");
                while (myNode.firstChild) {
                    myNode.removeChild(myNode.firstChild);
                }
                }
            // When the user clicks anywhere outside of the modal, close it
            window.onclick = function(event) {
            if (event.target == modal) {

                modal.style.display = "none";
                var myNode = document.getElementById("mbody");
                while (myNode.firstChild) {
                    myNode.removeChild(myNode.firstChild);
                }
                }
                }
        }

  }, ".result");






                    }