/*
AI-------------------------------------------------------------------
	The majority of WebSocket events will take place in this
	JS file.
-------------------------------------------------------------------AI
*/

websocket_url = ws_or_wss + window.location.host
	+'/ws/chat/' + room_id + '/';

/*
AI-------------------------------------------------------------------
	The following function opens a websocket with the current URL,
	sends messages to that websocket, receives and processes messages
	that are sent back from the server.
-------------------------------------------------------------------AI
*/
function startWebSocket(websocket_url) {
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
		var warning = data['warning'];
		var sender = data['sender'];
		var received_room_id = data['room_id'];
		if (username === sender) {
			// Below line adds the current chatroom to the top
			$('#' + received_room_id).parent().prepend($('#' + received_room_id));
			$('#chat-dialog').append(
			'<div class="message-container">'
			+ '<div class = "message message-sent">' + message + '</div>'
			+ '</div>');
			if (warning) {
				$('#chat-dialog').append(
				'<div class="message-container">'
				+ '<div class = "message message-received">' + warning + '</div>'
				+ '</div>');
			}

			$('#send-message').val('');

		} else {
			// The room that received the new message is open right now
			if (received_room_id === room_id) {
				$('#'+received_room_id).css('font-weight', 'bold');
				$('#'+received_room_id).parent().parent().prepend($('#'+received_room_id).parent());
				$('#chat-dialog').append(
				'<div class="message-container">'
				+ '<div class = "message message-received">' + message + '</div>'
				+ '</div>');
				if (warning) {
					$('#chat-dialog').append(
					'<div class="message-container">'
					+ '<div class = "message message-received">' + warning + '</div>'
					+ '</div>');
				}
			}
			// The room containing the new message is a different room from the current one
			else {
				$('#'+received_room_id).css('font-weight', 'bold');
				$('#'+received_room_id).parent().parent().prepend($('#'+received_room_id).parent());
			}
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
				'message': message,
				'room_id': room_id,
			}));
		}
	});
}

/*
AI-------------------------------------------------------------------
	When the document is loaded, start the websocket connection.
	The webpage should load the latest 50 messages in a particular
	group chat. When that is done, scroll down to the bottom to
	reveal the latest messages.
-------------------------------------------------------------------AI
*/
$(function() {
	startWebSocket(websocket_url);
	document.getElementById('chat-dialog').scrollTop
		= document.getElementById('chat-dialog').scrollHeight;
	$active_room = $("#" + room_id);
	$active_room.css("background", "#E0E0E0");

});

// Animation to slide up chat window and slide down user list in mobile devices
$('.fa-arrow-left').click(function() {
	$(this).hide();
	$('.chat-container').slideUp();
	$('.chatroom-list').slideDown();
	$('.room-name').hide();
});
