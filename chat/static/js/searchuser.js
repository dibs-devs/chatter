//This script fetches a list of registered users
//and displays it dynamically on the index page search bar.

//This function sends an AJAX request to fetch an array
//of users in the django backend.
//line 7 is a short form of saying 'The webpage has fully loaded.'
$(function() {
	$.ajax({
		//The url to send the request to
		url: '/ajax/users_list/', 
		/*If the request succeeds, there is data sent back from
		the server in JSON format. The AJAX function calls in two 
		functions with the array of users. The functions are defined below.*/
		success: function( data ) {
			populate(data.userslist);
			linkuser(data.userslist);
		}
	});
});

/*This uses the JQuery UI Plugin to filter and autocomplete the list of users
as you search for a user. Of course, this isn't exactly customizable CSS-wise.
*/
function populate(array) {
	$('#searchbar').autocomplete({source: array});
}

/*Once the user has typed in a valid username, this function takes the user
to a new URL which is the chatroom between the two users.*/
function linkuser(array) {
	$('#searchbar').keyup(function(e) {
		if (e.which === 13) {
			if (array.includes($(this).val())) {
				$('#user-selected').trigger('click');
			}
			else {
				alert('Please enter a valid User to chat with.');
			}
		}
	});

	$('#user-selected').click( function() {
		if (array.includes($('#searchbar').val())) {
				location.href = 'http://' + window.location.host + '/' 
				+ 'chat/' +  
				$('#searchbar').val() + '/';
			}
			else {
				alert('Please enter a valid User to chat with.');
			}
		
	});
}