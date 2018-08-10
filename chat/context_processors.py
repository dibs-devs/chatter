from django.contrib.auth.decorators import login_required
from .models import *

@login_required
def get_chatroom_list(request):
	rooms_list = Room.objects.filter(members=request.user).order_by('-date_modified')
	return ({'rooms_list': rooms_list})