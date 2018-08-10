/*
AI-------------------------------------------------------------------
	The majority of WebSocket events will take place in this
	JS file.
-------------------------------------------------------------------AI
*/

websocket_url = ws_or_wss + window.location.host
	+'/ws/chat/' + room_uuid + '/';

function startWebSocket(websocket_url) {
	var chatSocket =  new WebSocket(
		websocket_url
	);

	chatSocket.onopen = function(e) {
		console.log('Websocket connected.');
	}

	chatSocket.onmessage=function(e) {
		console.log('received data!');
		var data = JSON.parse(e.data);
		console.log(data);
		var message = data['message'];
		console.log(message);
		$('#chat-dialog').append(
			'<div class="message-container">'
			+ '<div class = "sent-message">' + message + '</div>'
			+ '</div>');
		$('#send-message').val('');
		document.getElementById('chat-dialog').scrollTop
		= document.getElementById('chat-dialog').scrollHeight;
	}

	chatSocket.onclose=function() {
		console.log('WebSocket disconnected.');
		setTimeout(function(){startWebSocket(websocket_url)}, 5000);
	}

	$('#send-message').keyup(function(e) {
		if (e.which === 13) {
			$('#send-button').trigger('click');
		}
	});

	$('#send-button').click( function() {
		console.log('Send button clicked');
		var message = $('#send-message').val();
		if (message !== '') {
			chatSocket.send(JSON.stringify({
				'message': message,
			}));
		}
	});
}

$(function() {
	console.log('ready!');
	startWebSocket(websocket_url);
});
