from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import *
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from django.utils.safestring import mark_safe
import bleach
from datetime import datetime

#Time libraries used to record the time when the user disconnects.
#New messages will be derived from this time in the view.
from django.utils.timezone import now

class ChatConsumer(AsyncWebsocketConsumer):

    '''
    AI-------------------------------------------------------------------
        Database Access methods below
    -------------------------------------------------------------------AI
    '''

    @database_sync_to_async
    def get_room_list(self, user):
        return Room.objects.filter(members=user)

    @database_sync_to_async
    def get_room(self, room_id):
        return Room.objects.get(id=room_id)

    @database_sync_to_async
    def update_user_access_time(user):
        user.last_visit = datetime.now()
        user.save()

    @database_sync_to_async
    def save_message(self, room, user, message):
        '''
        AI-------------------------------------------------------------------
            1. Select the Room
            2. Select the user who sent the message
            3. Select the message to be saved
            4. Save message
            5. Set room update time to message date_modified
        -------------------------------------------------------------------AI
        '''
        room = room
        sender = user
        text = message
        new_message = Message(room=room, sender=sender, text=text)
        new_message.save()
        room.date_modified = new_message.date_modified
        room.save()

    '''
    AI-------------------------------------------------------------------
        WebSocket methods below
    -------------------------------------------------------------------AI
    '''
    async def connect(self):
        self.user = self.scope['user']
        self.room_list = await self.get_room_list(self.user)

        #This if clause might be redundant.
        if (self.user.is_authenticated):
            for room in self.room_list:
                room_group_name = 'chat_%s' % room.id
                await self.channel_layer.group_add(
                    room_group_name,
                    self.channel_name
                )
            await self.accept()
        else:
            await self.disconnect(403)

    async def disconnect(self, close_code):
        for room in self.room_list:
            room_group_name = 'chat_%s' % room.id
            await self.channel_layer.group_discard(
                room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        username = self.user.username

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        room_id = text_data_json['room_id']

        try:
            room = await self.get_room(room_id)
            room_group_name = 'chat_%s' % room.id
        except Exception as ex:
            template = 'An exception of type {} occured. Arguments: \n{}'
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            await self.disconnect(200)

        self.message_safe = bleach.clean(message)
        message_harmful = (self.message_safe != message)

        await self.save_message(room, self.user, self.message_safe)

        if message_harmful:
            warning = "Your message has been escaped due to security reasons.\
             For more information, see \
             https://en.wikipedia.org/wiki/Cross-site_scripting"
        else:
            warning = ''

        await self.channel_layer.group_send(
            room_group_name,
            {
                'type': 'send_to_websocket',
                'message': self.message_safe,
                'warning': warning,
                'sender': username,
                'room_id': room_id,
            }
        )

    async def send_to_websocket(self, event):
        message = event['message']
        warning = event['warning']
        sender = event['sender']
        room_id = event['room_id']
        if warning == '':
            await self.send(text_data=(json.dumps({
                'message': message,
                'sender': sender,
                'room_id': room_id,
                })))
        else:
            await self.send(text_data=(json.dumps({
                'message': message,
                'sender': sender,
                'warning': warning,
                'room_id': room_id
                })))
