from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
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