from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth import logout, get_user_model
from .models import *
from django.db.models import Count
from django.core.exceptions import PermissionDenied

@login_required
def index(request):
	return render(request, 'django_chatter/index.html')

# This fetches a chatroom given the room ID if a user diretly wants to access the chat.
@login_required
def chatroom(request, uuid):
	user = get_user_model().objects.get(username=request.user)
	room = Room.objects.get(id=uuid)
	if room:
		if user in room.members.all():
			latest_messages = room.message_set.all().order_by('-id')[:50]
			for message in latest_messages:
				message.recipients.add(user)
			return render(request, 'django_chatter/chat-window.html',
				{'room_uuid_json': uuid,
				'latest_messages': latest_messages,
				'room_name': room.__str__()}
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
	rooms_with_member_count = Room.objects.annotate(num_members = Count('members'))
	user = get_user_model().objects.get(username=request.user)
	target_user = get_user_model().objects.get(username=request.POST.get('target_user'))

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
		if final_room.exists():
			if len(final_room) == 1:
				room_url = final_room[0].id
				return JsonResponse({'room_url': room_url})
			else:
				raise AttributeError(
					'Multiple two-member rooms for \
					{} and {} exists.'.format(user, target_user)
					)
		else:
			new_room=Room()
			new_room.save()
			new_room.members.add(user)
			new_room.members.add(target_user)
			new_room.save()
			new_room_id_json={'room_url': new_room.id}
			return JsonResponse(new_room_id_json)
