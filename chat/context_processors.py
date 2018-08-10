from .models import *
def get_chatroom_list(request):
	if request.user:
		if request.user.is_authenticated:
			rooms_list = Room.objects.filter(members=request.user).order_by('-date_modified')
			return ({'rooms_list': rooms_list})
		else:
			return ({})
	else:
		return ({})
