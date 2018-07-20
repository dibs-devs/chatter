from channels.generic.websocket import AsyncWebsocketConsumer
import json
from . import *
from django.contrib.auth.models import User
from channels.db import database_sync_to_async

#I used websocket initially but realized AJAX is much simpler. 
# This is just template code for the future now.
class SearchUser(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        users = await self.get_all_users()
        users = list(users)
        users_json = json.dumps({'userslist': users})
        await self.send(users_json)

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print (text_data_json)
        
    @database_sync_to_async
    def get_all_users(self):
        return User.objects.values_list('username', flat = True)