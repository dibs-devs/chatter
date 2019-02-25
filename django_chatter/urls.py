from django.urls import path
from . import views

# Defined namespace for use on all templates
app_name = 'django_chatter'

urlpatterns = [
	path('', views.index, name = "index"),
	path('chat/<str:uuid>/', views.chatroom, name = "chatroom"),

	#AJAX paths
	path('ajax/users-list/', views.users_list, name = "users_list"),
	path('ajax/get-chat-url/', views.get_chat_url, name = "get_chat_url"),
]
