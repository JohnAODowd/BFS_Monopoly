var c = document.getElementById("canvasProperty");
var ctx = c.getContext("2d");

var xmlhttp = new XMLHttpRequest();
xmlhttp.open('GET', "../Server/monopoly/properties.json", true);
xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == 4) {
        if(xmlhttp.status == 200) {
            var json = JSON.parse(xmlhttp.responseText);
            console.log(json);

			// Border
			ctx.beginPath();
			ctx.rect(9,9,122,32);
			ctx.fill();

			ctx.beginPath();
			ctx.rect(4,5,132,170);
			ctx.lineWidth="1";
			ctx.strokeStyle="black";
			ctx.stroke();

			// Colour 
			ctx.beginPath();
			ctx.rect(10,10,120,30);
			ctx.fillStyle = json['properties']['brown1']['colourHex'];
			ctx.fill();

			// Setup Title
			ctx.font = "12px Arial"; 
			ctx.fillStyle = "black";
			ctx.textAlign = "center";
			ctx.fillText(json['properties']['brown1']['name'], 70, 35);

			// Setup Title / Rent
			ctx.font = "10px Arial"; 
			var rentVal = json['properties']['brown1']['rent'].toString();
			ctx.fillText( "Rent $".concat(rentVal), 70, 55);
			ctx.fillText("Title Deed", 70, 20);

			// Setup bottom of the card
			var hotelVal = json['properties']['brown1']['hotel'].toString();
			ctx.fillText( "With HOTEL $".concat(hotelVal), 70, 115);

			var mortVal = json['properties']['brown1']['mortgage'].toString();
			ctx.fillText( "Mortgage Value $".concat(mortVal), 70, 130);

			/*
			var houseVal = Property.houseprice.toString();
			ctx.fillText("Houses Cost $".concat(houseVal).concat(" each"), 70, 145);
			ctx.fillText("Hotels, $".concat(houseVal).concat(" plus 4 houses"), 70, 160);
			*/

			// Setup House Values
			ctx.textAlign = "left";
			ctx.fillText( "With 1 House ", 10, 70);
			ctx.fillText( "With 2 Houses ", 10, 80);
			ctx.fillText( "With 3 Houses ", 10, 90);
			ctx.fillText( "With 4 Houses ", 10, 100);

			ctx.textAlign = "right";
			ctx.fillText( json['properties']['brown1']['house1'], 130, 70);
			ctx.fillText( json['properties']['brown1']['house2'], 130, 80);
			ctx.fillText( json['properties']['brown1']['house3'], 130, 90);
			ctx.fillText( json['properties']['brown1']['house4'], 130, 100);

         }
    }
};
xmlhttp.send(null);
