/*
AI-------------------------------------------------------------------
	This script makes an AJAX call to get a list of registered
	users. After that, the list is displayed dynamically using
	JQuery UI so that when a user is typing a username, the user
	can access these recipient users.
-------------------------------------------------------------------AI
*/

//Global variable to modify HREF to tailor to secure or non-secure connections.
var http_or_https = window.location.protocol == "https:" ? "https://" : "http://";
var ws_or_wss = window.location.protocol == "https:" ? "wss://" : "ws://";

/*
AI-------------------------------------------------------------------
	This uses the JQuery UI Plugin to filter and autocomplete
	the list of users as you search for a user in the searchbar.
	Of course, this isn't exactly customizable CSS-wise.
-------------------------------------------------------------------AI
*/
function populate( array ) {
	$('#searchbar').autocomplete({source: array});
}

/*
AI-------------------------------------------------------------------
	This function sends the logged in user to a new URL that contains
	the chat between the user and the destination user they
	searched for.
-------------------------------------------------------------------AI
*/
function linkuser( array ) {
	$('#searchbar').keyup(function(e) {
		if (e.which === 13) {
			if (array.includes($(this).val())) {
				$('#user-selected').trigger('click');
			}
			else {
				alert('Please enter a valid user to chat with.');
			}
		}
	});

	//Once the user presses the Go button or the enter button,
	//this codeblock is run to validate and connect the user
	//to the recipient.
	$('#user-selected').click( function() {
		if (array.includes($('#searchbar').val())) {
				$.ajax({
					// url: '/chat/ajax/get-chat-url/',
					url: get_chat_url,
					type: 'POST',
					data: {
						'target_user': $('#searchbar').val(),
						'csrfmiddlewaretoken': jQuery(
							"[name=csrfmiddlewaretoken]"
							).val(),
					},
					success: function (data) {
						location.href=http_or_https + window.location.host + chatter_index
						+ 'chat/' + data.room_url + '/';
					}
				});
			}
			else {
				alert('Please enter a valid User to chat with.');
			}

	});
}

/*
AI-------------------------------------------------------------------
	Once the page loads, the following function is run.
	It fetches users list and calls the populate function followed
	by linkuser function, which takes the current user to the chat
	page with the destination user.
-------------------------------------------------------------------AI
*/
$(function() {
	$.ajax({
		//The url to send the request to
		// url: '/chat/ajax/users-list/',
		url: get_user_url,
		/*If the request succeeds, there is data sent back from
		the server in JSON format. The AJAX function calls in two
		functions with the array of users.*/
		success: function( data ) {
			populate(data.userslist);
			linkuser(data.userslist);
		}
	});
});
