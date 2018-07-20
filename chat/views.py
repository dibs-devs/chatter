from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth import logout
from django.contrib.auth.models import User


# Create your views here.
@login_required
def index(request):
	user_list = User.objects.all()

	return render(request, 'chat/index.html', {'user_list': user_list})

def custom_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('chat:index'))

@login_required
def users_list(request):
	users = list(User.objects.values_list('username', flat = True))
	users_list_json = {'userslist': users}
	return JsonResponse(users_list_json)

@login_required
def chatroom(request, username):
	if username in list(User.objects.values_list('username', flat = True)):
		return render(request, 'chat/chatroom.html')
	else:
		raise Http404("Invalid User! What are you even trying?")