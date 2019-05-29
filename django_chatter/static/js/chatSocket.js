/*
AI-------------------------------------------------------------------
	The majority of WebSocket events will take place in this
	JS file.

	Depends on:
		dateFormatter.js
		websocketHelpers.js
-------------------------------------------------------------------AI
*/

//Global variable to modify HREF to tailor to secure or non-secure connections.
var ws_or_wss = window.location.protocol == "https:" ? "wss://" : "ws://";

websocket_url = ws_or_wss + window.location.host
	+'/ws/django_chatter/chatrooms/' + room_id + '/';



/*
AI-------------------------------------------------------------------
	The following opens a websocket with the current URL,
	sends messages to that websocket, receives and processes messages
	that are sent back from the server.
-------------------------------------------------------------------AI
*/
var chatSocket =  new WebSocket(
	websocket_url
);
//Notify when the websocket is connected.
chatSocket.onopen = function(e) {
	console.log('Websocket connected.');
}

/*
AI-------------------------------------------------------------------
	When a message is received:
	1) Parse the message.
	2) Find out who the sender is.
	3) Store the message text.
	4) If there is a warning, store it.
	5) If the message is sent by the user logged into the session,
		apply the correct classes to the message so it's displayed
		to the right.
	6) If the message is sent by a different user, apply the correct
		classes to the message so it's displayed to the left.
	7) If there are warnings in step 5 and 6, append it to the dialog
		after the corresponding message.
	8) Clear the input textarea for the current user to send a new
		chat message.
	9) After the messages have been rendered, scroll down to the bottom
		of the dialog to the latest messages that have been sent.
-------------------------------------------------------------------AI
*/
chatSocket.onmessage=function(e) {
	var data = JSON.parse(e.data);
	var message = data['message'];
	var sender = data['sender'];
	var received_room_id = data['room_id'];
  var date_created = dateFormatter(data['date_created']);

	// Below line adds the current chatroom to the top
	$last_room = $('#' + received_room_id);
	$last_room.parent().prepend($last_room);

	if (username === sender) {
		addSenderMessage(message, sender, received_room_id, date_created, 'append');
	}
	else {
		$last_room.find('.chat-list-item').css('font-weight', 'bold');
		addOpponentMessage(message, sender, received_room_id, date_created, 'append');
	}
	document.getElementById('chat-dialog').scrollTop
	= document.getElementById('chat-dialog').scrollHeight;
}

//Notify when the websocket closes abruptly.
chatSocket.onclose=function() {
	console.log('WebSocket disconnected.');
	//setTimeout(function(){startWebSocket(websocket_url)}, 5000);
}

//When the enter key is pressed on the textarea, trigger a click
//on the Send button.
$('#send-message').keyup(function(e) {
	if (e.which === 13) {
		$('#send-button').trigger('click');
	}
});

//When the Send button is clicked, check if its just an empty message (i.e. only spaces).
//If it is, don't send the message. Otherwise, send it to the websocket.
$('#send-button').click( function() {
	if ($.trim($("#send-message").val())) {
		var message = $('#send-message').val();
		chatSocket.send(JSON.stringify({
      'message_type': 'text',
			'message': message,
			'room_id': room_id,
			'sender': username
		}));
	}
});
