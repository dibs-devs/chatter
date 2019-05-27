/*
  This websocket connects to a group named by the current user. Whenever the current
  user is in a chatroom but a message appears in a different chatroom that the
  user belongs to, the user gets an alert and a snippet of that message displayed
  to them.

  dateFormatter.js
  websocketHelpers.js
*/

//Global variable to modify HREF to tailor to secure or non-secure connections.
var ws_or_wss = window.location.protocol == "https:" ? "wss://" : "ws://";

websocket_url = ws_or_wss + window.location.host
	+'/ws/django_chatter/users/' + username + '/'; // username variable in chat-window.html



/*
AI-------------------------------------------------------------------
	The following opens a websocket with the current URL,
	sends messages to that websocket, receives and processes messages
	that are sent back from the server.
-------------------------------------------------------------------AI
*/
var alertSocket =  new WebSocket(
	websocket_url
);
//Notify when the websocket is connected.
alertSocket.onopen = function(e) {
	console.log('Alert socket connected.');
}

/*
AI-------------------------------------------------------------------
	When a new alert arrives, add it to the chatroom preview
-------------------------------------------------------------------AI
*/
alertSocket.onmessage = function(e) {
	var data = JSON.parse(e.data);
	var message = data['message'];
	var sender = data['sender'];
	var received_room_id = data['room_id'];
  var date_created = dateFormatter(data['date_created']);

	// Below line adds the chatroom that got a new message to the top
	$last_room = $('#' + received_room_id);
	$last_room.parent().prepend($last_room);

  // Highlight it
  $last_room.find('.chat-list-item').css('font-weight', 'bold');

  // Add the new message preview
  updateOpponentMessagePreview(received_room_id, sender, message);
}

//Notify when the websocket closes abruptly.
alertSocket.onclose = function() {
	console.log('Alert WebSocket disconnected.');
	//setTimeout(function(){startWebSocket(websocket_url)}, 5000);
}
