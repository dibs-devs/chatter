from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth import logout, get_user_model
from django.core.exceptions import PermissionDenied
from django.conf import settings

from .models import *
from .utils import create_room

@login_required
def index(request):
	rooms_list = Room.objects.filter(members=request.user).order_by('-date_modified')
	if rooms_list.exists():
		latest_room_uuid = rooms_list[0].id
		return chatroom(request, latest_room_uuid)
	else:
		return render(request, 'django_chatter/index.html')

# This fetches a chatroom given the room ID if a user diretly wants to access the chat.
@login_required
def chatroom(request, uuid):
	try:
		base_template = settings.CHATTER_BASE_TEMPLATE
	except AttributeError as e:
		print ("(Optional) settings.CHATTER_BASE_TEMPLATE not found. Have you "
		"set it to point to your base template in your settings file?")
		base_template = 'django_chatter/base.html'
	user = get_user_model().objects.get(username=request.user)
	try:
		room = Room.objects.get(id=uuid)
	except Exception as e:
		print (e)
		raise Http404("Sorry! What you're looking for isn't here.")
	if room:
		if user in room.members.all():
			latest_messages = room.message_set.all().order_by('-id')[:50]
			for message in latest_messages:
				message.recipients.add(user)
			return render(request, 'django_chatter/chat-window.html',
				{'room_uuid_json': uuid,
				'latest_messages': latest_messages,
				'room_name': room.__str__(),
				'base_template': base_template,
				}
			)
		else:
			raise Http404("Sorry! What you're looking for isn't here.")
	else:
		raise Http404("Sorry! What you're looking for isn't here.")

#The following functions deal with AJAX requests
@login_required
def users_list(request):
	users = list(get_user_model().objects.values_list('username', flat = True))
	users_list_json = {'userslist': users}
	return JsonResponse(users_list_json)

@login_required
def get_chat_url(request):
	user = get_user_model().objects.get(username=request.user)
	target_user = get_user_model().objects.get(username=request.POST.get('target_user'))

	'''
	AI-------------------------------------------------------------------
		Use the util room creation function to create room for one/two
		user(s). This can be extended in the future to add multiple users
		in a group chat.
	-------------------------------------------------------------------AI
	'''
	if (user == target_user):
		room_id = create_room([user])
	else:
		room_id = create_room([user, target_user])
	new_room_id_json={'room_url': room_id}
	return JsonResponse(new_room_id_json)
