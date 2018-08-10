from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import *
from django.db.models import Count, Q
import json
from django.utils.safestring import mark_safe
from django.core.exceptions import PermissionDenied


# Create your views here.
@login_required
def index(request):
	return render(request, 'chat/index.html')

def custom_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('chat:index'))

@login_required
def chatroom(request, uuid):
	room = Room.objects.get(id=uuid)
	if room:
		user = User.objects.get(username=request.user)
		if user in room.members.all():
			return render(request, 'chat/chat-window.html', 
				{'room_uuid_json': mark_safe(json.dumps(uuid))})
		else:
			raise PermissionDenied()
	else:
		raise Http404("The room you searched for does not exist.")

#The following functions deal with AJAX requests

@login_required
def users_list(request):
	users = list(User.objects.values_list('username', flat = True))
	users_list_json = {'userslist': users}
	return JsonResponse(users_list_json)

@login_required
def get_chat_url(request):
	print ('ajax call initiated to get chat URL!')
	rooms_with_member_count = Room.objects.annotate(num_members = Count('members'))
	user = User.objects.get(username=request.user)
	target_user = User.objects.get(username=request.POST.get('target_user'))
	print ('logged in user:', user)
	print ('target user:', target_user)

	'''
	AI-------------------------------------------------------------------
		If the user is trying to chat with themselves, check if the 
		room with that user only exists. 
		If it does, return that room's ID to for URL with it.
		If it doesn't, create a room with that user in it and return
		the new room's ID.
	-------------------------------------------------------------------AI
	'''
	if (user == target_user):
		#QuerySet of rooms with one user
		rooms_for_one = rooms_with_member_count.filter(
			num_members__gte=1).filter(num_members__lte=1)
		#QuerySet of room(s) with the particular logged in user
		final_room = rooms_for_one.filter(members=user)
		if final_room.exists():
			if len(final_room) == 1:
				room_url = final_room[0].id
				return JsonResponse({'room_url': room_url})
			else:
				raise AttributeError(
					'Multiple one-member rooms for the same user exist.'
					)
		else:
			new_room=Room()
			new_room.save()
			new_room.members.add(user)
			new_room.save()
			new_room_id_json={'room_url': new_room.id}
			return JsonResponse(new_room_id_json)
		'''
		AI-------------------------------------------------------------------
			If the user is trying to chat with another user, check if the
			right room already exists.
			If the room exists, return the room's ID to form the
			unique room URL.
			If the room doesn't exist, make the room, put the two users in
			that room, and return the new room's ID to form the URL.
		-------------------------------------------------------------------AI
		'''
	else:
		room_for_two = rooms_with_member_count.filter(
			num_members__gte=2).filter(num_members__lte=2)
		final_room = room_for_two.filter(
			members=user).filter(members=target_user)
		print (final_room)
		if final_room.exists():
			if len(final_room) == 1:
				room_url = final_room[0].id
				return JsonResponse({'room_url': room_url})
			else:
				print (user)
				print (target_user)
				raise AttributeError(
					'Multiple two-member rooms for the above users exists.'
					)
		else:
			new_room=Room()
			new_room.save()
			new_room.members.add(user)
			new_room.members.add(target_user)
			new_room.save()
			new_room_id_json={'room_url': new_room.id}
			return JsonResponse(new_room_id_json)
