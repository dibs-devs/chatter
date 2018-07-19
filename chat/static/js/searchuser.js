//Search Users up to chat with them
var searchSocket = new WebSocket(
	'ws://' + window.location.host + '/search/'
	);

searchSocket.onmessage = function(e) {
	var data = JSON.parse(e.data);
	console.log(data);
}

searchSocket.onclose = function(e) {
	console.error('Chat socket closed unexpectedly');
}

$('#userselected').click(function() {
	var user = $('#selectuser').val();
	console.log(user);
	searchSocket.send(JSON.stringify(user));
})

