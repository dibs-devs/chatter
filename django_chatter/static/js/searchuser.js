/*
AI-------------------------------------------------------------------
	This script makes an AJAX call to get a list of registered
	users. After that, the list is displayed dynamically using
	JQuery Select2 so that when a user is typing a username, the user
	can access these recipient users.
-------------------------------------------------------------------AI
*/

//Global variable to modify HREF to tailor to secure or non-secure connections.
var http_or_https = window.location.protocol == "https:" ? "https://" : "http://";
var ws_or_wss = window.location.protocol == "https:" ? "wss://" : "ws://";

/*
AI-------------------------------------------------------------------
	Once the page loads, the following function is run.
	It fetches users list populates the select element with
	the list
-------------------------------------------------------------------AI
*/
$(function() {

	$.ajax({
		//The url to send the request to
		// url: '/chat/ajax/users-list/',
		url: get_user_url,
		/*If the request succeeds, there is data sent back from
		the server in JSON format: [{'id': int, 'text': str}...]*/
		success: function( data ) {
			// populate(data.userslist);
			// linkuser(data.userslist);
			$('.select-chat-user').select2({
				placeholder: 'Start chat',
				data: data,
				width: 'resolve',
			});
		}
	});
});


// If no option is selected in the user search form, then do nothing
$('.search-form').submit(function(e) {
	if ($('.select-chat-user option:selected').text() == "") {
		e.preventDefault();
	}
});
