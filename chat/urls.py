from django.urls import path
from . import views

# Defined namespace for use on all templates
app_name = 'chat'

urlpatterns = [
	path('chat/', views.index, name = "index"),
	path('chat/accounts/logout/', views.custom_logout, name = "logout"),
	path('chat/<str:uuid>/', views.chatroom, name = "chatroom"),

	#AJAX paths
	path('chat/ajax/users-list/', views.users_list, name = "users_list"),
	path('chat/ajax/get-chat-url/', views.get_chat_url, name = "get_chat_url"),
]