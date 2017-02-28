/*
This file is used to intercept form submission to the server so we can process the header ourselves
*/

(function($){
	$(function(){

		$(document).ready(function(){
			// set event listeners
			// $('#host-form').on('submit', function(e){
			// 	// here we send an AJAX request to the server for an html file
			// 	// this file will include a key in its header
			// 	// we append this new processed html to the page body
			// 	e.preventDefault();
			// 	$.ajax({

			// 		url : '/newpage',
			// 		type : 'POST',
			// 		data : requestString,
			// 		dataType : "text",
			// 		processData : false,
			// 		contentType : false,
			// 		success : function(completeHtmlPage) {
			// 		    alert("Success");
			// 		    $("html").empty();
			// 		    $("html").append(completeHtmlPage);

			// 		},
			// 		error : function() {
			// 		    alert("error in loading");
			// 		}

			// 	});
			// });
		});

  	}); // end of document ready
})(jQuery); // end of jQuery name space