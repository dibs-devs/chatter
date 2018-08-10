from django.urls import path

from . import consumers

websocket_urlpatterns = [
	path('search/', consumers.SearchUser),
	path('ws/chat/<str:room_uuid>/', consumers.ChatConsumer),
]