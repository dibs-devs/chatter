from django.urls import path
from . import views

# Defined namespace for use on all templates
app_name = 'chat'

urlpatterns = [
	path('', views.index, name = "index"),
	path('accounts/logout/', views.custom_logout, name = "logout"),
	path('chat/<str:uuid>/', views.chatroom, name = "chatroom"),

	#AJAX paths
	path('ajax/users-list/', views.users_list, name = "users_list"),
	path('ajax/get-chat-url/', views.get_chat_url, name = "get_chat_url"),
]