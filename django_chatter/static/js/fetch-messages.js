// This module fetches past messages once the user scrolls
// to top.


var didScroll = false;

$('#chat-dialog').scroll(function() {
    didScroll = true;
});

setInterval(function() {
    if ( didScroll ) {
        didScroll = false;
        // console.log("scrolled"); // This works.
        // Check your page position and then
        // Load in more results
    }
}, 250);
