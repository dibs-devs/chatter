from django.conf import settings
from channels.testing import WebsocketCommunicator
import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from django_chatter.models import Room
from chatter.routing import application

import json


TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_chat_consumer():
    settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
    room = Room.objects.create()
    user = get_user_model().objects.create(username="user0")
    room.members.add(user)
    room.save()
    client = Client()
    client.force_login(user=user)
    communicator = WebsocketCommunicator(
        application, f"/ws/chat/{room.id}/",
        headers=[(
                b'cookie',
                f'sessionid={client.cookies["sessionid"].value}'.encode('ascii')
            )]
        )
    connected, subprotocol = await communicator.connect()
    assert connected
    data = json.dumps({
        'message': "Hello!",
        'sender': user.username,
        'room_id': str(room.id),
        })
    await communicator.send_to(text_data=data)
    response = await communicator.receive_from()
    response = json.loads(response)
    assert response['message'] == "Hello!"
    assert response['sender'] == "user0"
    assert response['room_id'] == str(room.id)
    await communicator.disconnect()
