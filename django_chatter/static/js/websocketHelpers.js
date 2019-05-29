/*
	Takes a string and returns it wrapped around a div with
	class: 'message-container'
*/
function addMessageContainerDiv(inner) {
	return '<div class="message-container">' + inner + '</div>';
}

function addSentReducedTopMarginDiv(inner) {
	return '<div class = "message message-sent sent-reduced-top-margin">'
		+ inner + '</div>';
}

function addSentReducedBottomMarginDiv(inner) {
	return '<div class = "message message-sent sent-reduced-bottom-margin">'
		+ inner + '</div>';
}

function addMessageReceivedContainerDiv(inner) {
	return '<div class = "message message-received">' + inner + '</div>';
}

function addMessageReceivedDateCreatedContainer(inner) {
	return '<div class = "message message-received message-date-created message-received-date-created">'
		+ inner + '</div>';
}

// The following two functions take in a room's UUID and adds the new message to its preview.
function updateSenderMessagePreview(room_id, message) {
	// Update the message preview on the chatoom-list
	$("#" + room_id)
		.find('.chat-list-last-message')
		.text("You: " + message);
}

function updateOpponentMessagePreview(room_id, sender, message) {
	// Update the message preview on the chatoom-list
	$("#" + room_id)
		.find('.chat-list-last-message')
		.text(sender + ": " + message);
}


function addSenderMessage(
													message,
													sender,
													received_room_id,
													date_created,
													append_or_prepend
	) {

	// Add sender's message to the bottom of the chat window. this is relevant on
	// websocket messages
	if (append_or_prepend == 'append') {
		$last_message = $('.message').not('.message-date-created').last();

		// group the message bubble aesthetically
		if ($last_message.hasClass('message-sent')) {
			$last_message.addClass('sent-reduced-bottom-margin');

			$('#chat-dialog').append(
				addMessageContainerDiv(
					addSentReducedTopMarginDiv(message)
					+ '<div class = "message message-sent message-date-created">'
						+ date_created
					+ '</div>'
				)
			);
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
		}

		updateSenderMessagePreview(received_room_id, message);
	}

	else if (append_or_prepend == 'prepend') {
		$first_message = $('.message').not('.message-date-created').first();
		if ($first_message.hasClass('message-sent')) {
			$first_message.addClass('sent-reduced-top-margin');

			$('#chat-dialog').prepend(
				addMessageContainerDiv(
					addSentReducedBottomMarginDiv(message)
					+ '<div class = "message message-sent message-date-created">'
						+ date_created
					+ '</div>'
				)
			);
		}
		else {
			$('#chat-dialog').prepend(
				addMessageContainerDiv(
					'<div class = "message message-sent">'
						+ message
					+ '</div>'
					+ '<div class = "message message-sent message-date-created">'
						+ date_created
					+ '</div>'
				)
			);
		}
	}

	$('#send-message').val('');
}

function addOpponentMessage(
														message,
														sender,
														received_room_id,
														date_created,
														append_or_prepend
) {

	// If we're appending to the end of the chat
	if (append_or_prepend == "append") {
		$last_message = $('.message').not('.message-date-created').last();
		// If the last message has been sent by the opposition
		if ($last_message.hasClass('message-received')) {
			// if (received_room_id === room_id) {
			$last_message.addClass('received-reduced-bottom-margin');
			$last_message.prev().hide(); // Hide the user bubble
			$last_message.css('margin-left', '45px'); // Compensate margin for user bubble
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
		}

		// Last message is sent by the sender and not opposition
		else {
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
		}

		updateOpponentMessagePreview(received_room_id, sender, message);
	}

	// If we're prepending to the front of the chat on message load
	else if (append_or_prepend == "prepend") {
		$first_message = $('.message').not('.message-date-created').first();
		// If the First message has been sent by the opposition
		if ($first_message.hasClass('message-received')) {
			// if (received_room_id === room_id) {
			$first_message.addClass('received-reduced-top-margin');
			$('#chat-dialog').prepend(
				addMessageContainerDiv(
					'<div class="message-received-container">'
						 + '<div class="receiver-bubble">'
							 + sender.charAt(0).toUpperCase()
						 + '</div>'
						 + '<div class = "message message-received received-reduced-bottom-margin">'
								+ message
						 + '</div>'
					 + '</div>'
					 + addMessageReceivedDateCreatedContainer(date_created)
				)
			);
		}

		// First message is sent by the sender and not opposition
		else {
			$('#chat-dialog').prepend(
				addMessageContainerDiv('<div class="message-received-container">'
							+ '<div class="receiver-bubble">'
								+ sender.charAt(0).toUpperCase()
							+ '</div>'
							+ addMessageReceivedContainerDiv(message)
						+ '</div>'
						+ addMessageReceivedDateCreatedContainer(date_created)
				)
			);
		}
	}
}
