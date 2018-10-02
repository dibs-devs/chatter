$(function() {
	$(window).resize(checkSize);
});

function checkSize() {
	if $(('.chat-container').css("display") == "inline-block") {
		'.chat-container'.show();
	}
}