// This module fetches past messages once the user scrolls
// to top.

var didScroll = false;

var pageNum = 2;

$('#chat-dialog').scroll(function() {
    didScroll = true;
});

setInterval(function() {
    if ( didScroll ) {
        didScroll = false;
        checkAndFetch();
    }
}, 250);


function checkAndFetch() {
  // Check your page position and then
  // Load in more results
  if ($('#chat-dialog').scrollTop() === 0) {
    // $first_message = $('.message').not('.message-date-created').first();

    // room_id is defined in the templates
    get_url = get_room_url + '?page=' + pageNum;
    fetch(get_url, {
      credentials: 'same-origin',
      headers: {
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    .then(response => {
      return response.json();
    })
    .then(function(myJson) {
      myJson.forEach(function (object) {
        savedScrollTop = $('#chat-dialog').scrollTop();
        message = object['message'];
        sender = object['sender'];
        received_room_id = object['received_room_id'];
        date_created = dateFormatter(object['date_created']);
        if (username === sender) {
          addSenderMessage(message, sender, received_room_id, date_created, 'prepend');
        }
        else {
          addOpponentMessage(message, sender, received_room_id, date_created, 'prepend');
        }

        // Keep increasing scrollTop so scrollbar remains in same position
        $first_message = $('.message').not('.message-date-created').first();
        $('#chat-dialog').scrollTop(savedScrollTop + $first_message.prop("scrollHeight"));
      });
      pageNum++;
    });
  }
}
