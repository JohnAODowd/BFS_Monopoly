var xmlhttp = new XMLHttpRequest();
xmlhttp.open('GET', "../Server/monopolyJSON/properties.json", true);
xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == 4) {
        if(xmlhttp.status == 200) {
            var json = JSON.parse(xmlhttp.responseText);
            console.log(json);

            var properties = json.properties;
            for(var i in properties)
            {

            console.log(properties[i]);

            var c = document.getElementById(properties[i]['name']);
			var _ctx = c.getContext("2d");

			// Border
			_ctx.beginPath();
			_ctx.rect(9,9,122,32);
			_ctx.fill();

			_ctx.beginPath();
			_ctx.rect(4,5,132,170);
			_ctx.lineWidth="1";
			_ctx.strokeStyle="black";
			_ctx.stroke();

			// Colour 
			_ctx.beginPath();
			_ctx.rect(10,10,120,30);
			_ctx.fillStyle = properties[i]['colourHex'];
			_ctx.fill();

			// Setup Title
			_ctx.font = "12px Arial"; 
			_ctx.fillStyle = "black";
			_ctx.textAlign = "center";
			_ctx.fillText(properties[i]['name'], 70, 35);

			// Setup Title / Rent
			_ctx.font = "10px Arial"; 
			var rentVal = properties[i]['rent'].toString();
			_ctx.fillText( "Rent $".concat(rentVal), 70, 55);
			_ctx.fillText("Title Deed", 70, 20);

			// Setup bottom of the card
			var hotelVal = properties[i]['hotel'].toString();
			_ctx.fillText( "With HOTEL $".concat(hotelVal), 70, 115);

			var mortVal = properties[i]['mortgage'].toString();
			_ctx.fillText( "Mortgage Value $".concat(mortVal), 70, 130);

			var houseVal = properties[i]['houseprice'].toString();
			_ctx.fillText("Houses Cost $".concat(houseVal).concat(" each"), 70, 145);
			_ctx.fillText("Hotels, $".concat(houseVal).concat(" plus 4 houses"), 70, 160);


			// Setup House Values
			_ctx.textAlign = "left";
			_ctx.fillText( "With 1 House ", 10, 70);
			_ctx.fillText( "With 2 Houses ", 10, 80);
			_ctx.fillText( "With 3 Houses ", 10, 90);
			_ctx.fillText( "With 4 Houses ", 10, 100);

			_ctx.textAlign = "right";
			_ctx.fillText( properties[i]['house1'], 130, 70);
			_ctx.fillText( properties[i]['house2'], 130, 80);
			_ctx.fillText( properties[i]['house3'], 130, 90);
			_ctx.fillText( properties[i]['house4'], 130, 100);
			}
         }
    }
};
xmlhttp.send(null);
