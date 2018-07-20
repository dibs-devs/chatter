from django.urls import path
from . import views

# Defined namespace for use on all templates
app_name = 'chat'

urlpatterns = [
	path('', views.index, name = "index"),
	path('accounts/logout/', views.custom_logout, name = "logout"),
	path('ajax/users_list/', views.users_list, name = "users_list"),
	path('chat/<str:username>/', views.chatroom, name = "chatroom"),
]