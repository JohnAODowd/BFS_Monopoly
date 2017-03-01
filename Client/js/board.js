/*
var xmlhttp = new XMLHttpRequest();
xmlhttp.open('GET', "../Server/monopoly/properties.json", true);
xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == 4) {
        if(xmlhttp.status == 200) {
            var json = JSON.parse(xmlhttp.responseText);
            console.log(json);

           	//code
			
         }
    }
};
xmlhttp.send(null);

*/

var c = document.getElementById("board");
var ctx = c.getContext("2d");