from channels.generic.websocket import AsyncWebsocketConsumer
import json
from . import *
from django.contrib.auth.models import User
from channels.db import database_sync_to_async

class SearchUser(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user = await self.get_user(text_data_json)
        print (user)
        
    @database_sync_to_async
    def get_user(self, data):
        return User.objects.filter(username__exact = data)