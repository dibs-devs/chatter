/*
AI-------------------------------------------------------------------
	The majority of WebSocket events will take place in this
	JS file.
-------------------------------------------------------------------AI
*/

//Global variable to modify HREF to tailor to secure or non-secure connections.
var http_or_https = window.location.protocol == "https:" ? "https://" : "http://";
var ws_or_wss = window.location.protocol == "https:" ? "wss://" : "ws://";

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
		Takes a string and returns it wrapped around a div with
		class: 'message-container'
	*/
	function addMessageContainerDiv(inner) {
		return '<div class="message-container">' + inner + '</div>';
	}

	function addReducedTopMarginDiv(inner) {
		return '<div class = "message message-sent sent-reduced-top-margin">'
			+ inner + '</div>';
	}

	function addMessageReceivedContainerDiv(inner) {
		return '<div class = "message message-received">' + inner + '</div>';
	}

	function addMessageReceivedDateCreatedContainer(inner) {
		return '<div class = "message message-received message-date-created message-received-date-created">'
			+ inner + '</div>';
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
    var date_created = dateFormatter(data['date_created']);

		// Below line adds the current chatroom to the top
		$last_room = $('#' + received_room_id);
		$last_room.parent().prepend($last_room);

		if (username === sender) {
			$last_message = $('.message').not('.message-date-created').last();
			if ($last_message.hasClass('message-sent')) {
				$last_message.addClass('sent-reduced-bottom-margin');

				$('#chat-dialog').append(
					addMessageContainerDiv(
						addReducedTopMarginDiv(message)
            + '<div class = "message message-sent message-date-created">'
              + date_created
            + '</div>'
					)
				);

				if (warning) {
					$('#chat-dialog').append(
						addMessageContainerDiv(
							addMessageReceivedContainerDiv(warning)
            + '<div class = "message message-received message-date-created">'
              + date_created
            + '</div>'
					)
				);
				}
			}
			else {
				$('#chat-dialog').append(
					addMessageContainerDiv(
						'<div class = "message message-sent">'
              + message
            + '</div>'
            + '<div class = "message message-sent message-date-created">'
              + date_created
            + '</div>'
					)
				);

				if (warning) {
					$('#chat-dialog').append(
						addMessageContainerDiv(
						  addMessageReceivedContainerDiv(warning)
	            + '<div class = "message message-received message-date-created">'
	              + date_created
	            + '</div>'
						)
					);
				}
			}


			$('#send-message').val('');

		} else {
				$last_message = $('.message').not('.message-date-created').last();

        // If the last message has been sent by the opposition
				if ($last_message.hasClass('message-received')) {
					// if (received_room_id === room_id) {
					$last_message.addClass('received-reduced-bottom-margin');
					$('#'+received_room_id).find('.chat-list-item').css('font-weight', 'bold');
					$('#'+received_room_id).parent().prepend($('#'+received_room_id));
					$('#chat-dialog').append(
						addMessageContainerDiv(
							'<div class="message-received-container">'
                 + '<div class="receiver-bubble">'
                   + sender.charAt(0).toUpperCase()
                 + '</div>'
  					     + '<div class = "message message-received received-reduced-top-margin">'
                    + message
                 + '</div>'
               + '</div>'
               + addMessageReceivedDateCreatedContainer(date_created)
						)
					);

					if (warning) {
						$('#chat-dialog').append(
							addMessageContainerDiv(
								addMessageReceivedContainerDiv(warning)
                + addMessageReceivedDateCreatedContainer(date_created)
							)
						);
					}
				}

        // Last message is not sent by the opposition
				else {
					$('#'+received_room_id).find('.chat-list-item').css('font-weight', 'bold');
					$('#'+received_room_id).parent().prepend($('#'+received_room_id));
					$('#chat-dialog').append(
						addMessageContainerDiv('<div class="message-received-container">'
                  + '<div class="receiver-bubble">'
                    + sender.charAt(0).toUpperCase()
                  + '</div>'
                  + addMessageReceivedContainerDiv(message)
                + '</div>'
                + addMessageReceivedDateCreatedContainer(date_created)
						)
					);

					if (warning) {
						$('#chat-dialog').append(
							addMessageContainerDiv(
								addMessageReceivedContainerDiv(warning)
	              + addMessageReceivedDateCreatedContainer(date_created)
							)
						);
					}
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
        'type': 'text',
				'message': message,
				'room_id': room_id,
			}));
		}
	});
}
