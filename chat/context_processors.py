from .models import *

def get_chatroom_list(request):
	if request.user:
		if request.user.is_authenticated:
			rooms_list = Room.objects.filter(members=request.user).order_by('-date_modified')
			rooms_with_unread = []
			for room in rooms_list:
				for message in room.message_set.all().order_by('-id')[:50]:
					if request.user not in message.recipients.all():
						rooms_with_unread.append(room.id)
						break
			return ({'rooms_list': rooms_list, 'rooms_with_unread': rooms_with_unread})
		else:
			return ({})
	else:
		return ({})
