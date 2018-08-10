from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
import json
from . import *
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync

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

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        print (self.scope['user'])
        #print (self.scope['url_route']['kwargs']['room_uuid'])
        self.room_id = self.scope['url_route']['kwargs']['room_uuid']
        self.room_group_name = 'chat_%s' % self.room_id
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_to_websocket',
                'message': message
            }
        )

    def send_to_websocket(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message,
            }))