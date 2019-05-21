from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth import logout, get_user_model
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from .models import Room, Message
from .utils import create_room

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def import_base_template():
	try:
		return settings.CHATTER_BASE_TEMPLATE
	except AttributeError as e:
		try:
			if settings.CHATTER_DEBUG == True:
				logger.info("django_chatter.views: "
				"(Optional) settings.CHATTER_BASE_TEMPLATE not found. You can "
				"set it to point to your base template in your settings file.")
		except AttributeError as e:
			logger.info("django_chatter.views: "
			"(Optional) settings.CHATTER_BASE_TEMPLATE not found. You can "
			"set it to point to your base template in your settings file.")
			logger.info("django_chatter.views: to turn off this message, set "
			"your settings.CHATTER_DEBUG to False.")
		return 'django_chatter/base.html'


class IndexView(LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		rooms_list = Room.objects.filter(members=request.user).order_by('-date_modified')
		if rooms_list.exists():
			latest_room_uuid = rooms_list[0].id
			return HttpResponseRedirect(
				reverse('django_chatter:chatroom', args=[latest_room_uuid])
			)
		else:
			# create room with the user themselves
			user = get_user_model().objects.get(username=request.user)
			room_id = create_room([user])
			return HttpResponseRedirect(
				reverse('django_chatter:chatroom', args=[room_id])
			)


# This fetches a chatroom given the room ID if a user diretly wants to access the chat.
class ChatRoomView(LoginRequiredMixin, TemplateView):
	template_name = 'django_chatter/chat-window.html'

	# This gets executed whenever a room exists
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		uuid = kwargs.get('uuid')
		try:
			room = Room.objects.get(id=uuid)
			user=get_user_model().objects.get(username=self.request.user)
		except Exception as e:
			logger.exception("\n\nException in django_chatter.views.ChatRoomView:\n")
			raise Http404("Sorry! What you're looking for isn't here.")
		all_members = room.members.all()
		if user in all_members:
			latest_messages = room.message_set.all().order_by('-id')[:50]
			if latest_messages.exists():
				message = latest_messages[0]
				message.recipients.add(user)
			if all_members.count() == 1:
				room_name = "Notes to Yourself"
			elif all_members.count() == 2:
				room_name = all_members.exclude(pk=user.pk)[0]
			else:
				room_name = room.__str__()
			context['room_uuid_json'] = kwargs.get('uuid')
			context['latest_messages'] = latest_messages
			context['room_name'] = room_name
			context['base_template'] = import_base_template()

			# Add rooms with unread messages
			rooms_list = Room.objects.filter(members=self.request.user)\
				.order_by('-date_modified')
			try:
				rooms_list = rooms_list[10]
			except Exception as e:
				pass
			rooms_with_unread = []
			# Go through each list of rooms and check if the last message was unread
			for room in rooms_list:
				try:
					message = room.message_set.all().order_by('-id')[0]
				except IndexError as e:
					continue
				if self.request.user not in message.recipients.all():
					rooms_with_unread.append(room.id)
			context['rooms_list'] = rooms_list
			context['rooms_with_unread'] = rooms_with_unread

			return context
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
