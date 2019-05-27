from django.urls import path

from . import consumers

websocket_urlpatterns = [
	path('ws/django_chatter/chatrooms/<str:room_uuid>/', consumers.ChatConsumer),
	path('ws/django_chatter/users/<str:username>/', consumers.AlertConsumer)
]
