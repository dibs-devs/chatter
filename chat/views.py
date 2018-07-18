from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import logout

# Create your views here.
@login_required
def index(request):
	return render(request, 'chat/index.html')


def custom_logout(request):
	print('Hello!')
	logout(request)
	return HttpResponseRedirect(reverse('chat:index'))