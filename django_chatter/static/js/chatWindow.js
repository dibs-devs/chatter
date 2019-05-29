/*
AI-------------------------------------------------------------------
	When the document is loaded, scroll down to the bottom to
	reveal the latest messages.

	Depends on: date-formatter.js
-------------------------------------------------------------------AI
*/
$(function() {

	// Bubble modifications on messages sent by same people on load
	messages = $('.message').not('.message-date-created');
	messages.each(function(index, el) {
    if (index !== messages.length - 1) {
			$current = messages.eq(index);
			$next = messages.eq(index + 1);
			if ($current.hasClass('message-received')) {
				if ($next.hasClass('message-received')) {
					$current.prev().hide(); // Hide the username bubble
					$current.css('margin-left', '45px'); // Add margin to make up for the absence of bubble
					$current.addClass('received-reduced-bottom-margin');
					$next.addClass('received-reduced-top-margin');
				}
			}
			else if ($current.hasClass('message-sent')) {
				if ($next.hasClass('message-sent')) {
					$current.addClass('sent-reduced-bottom-margin');
					$next.addClass('sent-reduced-top-margin');
				}
			}
    }
	});

	// Formats the time a message was sent in a more chat-style manner like Android Messages or Messenger
	times = $('.message-date-created');
	times.each(function(index, el) {
		$this = times.eq(index);
		time_human_readable = dateFormatter($this.text());
		$this.text(time_human_readable);
	});

	// Set the latest message as visible
	document.getElementById('chat-dialog').scrollTop
		= document.getElementById('chat-dialog').scrollHeight;


	// Mark active room with grey focus color
	$active_room = $("#" + room_id); // room_id from chat-window.html
	$active_room.css("background", "var(--bg-grey)");

	// Focus message input on load
	$('#send-message').focus();
});


// Animation to slide up chat window and slide down user list in mobile devices
$('#back-button').click(function() {
	$(this).hide();
	$('.dialog-container').hide(400, function() {
		$chatroom_list = $('.chatroom-list-container');
		$chatroom_list.css('width','100%');
		$chatroom_list.css('max-width', '100%');
		$chatroom_list.css('border', '2px solid var(--bg-grey)');
		$chatroom_list.show();
	});
});


// When user clicks on the chat dialog, focus the input
// and change chatroom-list text to normal if it was bold before
$('#chat-dialog').click(function() {
	$('#send-message').focus(); // Focus message input
	$('#' + room_id).find('.chat-list-item').css('font-weight', 'normal');
});


// Don't select the input field when user clicks on message to enable selecting
// text
$('.message').click(function(e) {
	e.stopPropagation();
});


// Change chatroom lists's room's font to normal on text input click
$('#send-message').click(function() {
	$('#' + room_id).find('.chat-list-item').css('font-weight', 'normal');
});

// When a user clicks on a message, show the time underneath that message
$('body').on('click', '.message-sent', function () {
	$(this).next().slideToggle(200);
});

$('.message-sent').click(function() {
	$(this).next().slideToggle(200);
});

$('body').on('click', '.message-received', function() {
	$this = $(this);
	if (!$this.hasClass('message-received-date-created'))
		$(this).parent().next().slideToggle(200);
});

$('.message-received').click(function() {
	$this = $(this);
	if (!$this.hasClass('message-received-date-created'))
		$(this).parent().next().slideToggle(200);
});
