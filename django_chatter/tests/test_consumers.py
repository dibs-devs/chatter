from channels.testing import WebsocketCommunicator
from channels.routing import ProtocolTypeRouter, URLRouter

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client
from django.utils.timezone import now, get_default_timezone_name
from django.utils import dateformat

from django_chatter.models import Room, Message
from chatter.routing import application, multitenant_application
import django_chatter.routing
from django_chatter.utils import ChatterMTMiddlewareStack

from functional_tests.data_setup_for_tests import set_up_data

import pytz
import pytest

TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_single_tenant_chat_consumer():
    settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
    set_up_data()
    room = Room.objects.create()
    user = get_user_model().objects.get(username="user0")
    room.members.add(user)
    room.save()
    client = Client()
    client.force_login(user=user)
    communicator = WebsocketCommunicator(
        application, f"/ws/chat/{room.id}/",
        headers=[
            (
                b'cookie',
                f'sessionid={client.cookies["sessionid"].value}'.encode('ascii')
            ),
            (b'host', b'localhost:8000')]
        )
    connected, subprotocol = await communicator.connect()
    assert connected
    data = {
        'type': 'text',
        'message': "Hello!",
        'sender': user.username,
        'room_id': str(room.id),
        }
    await communicator.send_json_to(data)
    response = await communicator.receive_json_from()
    assert response['message'] == "Hello!"
    assert response['sender'] == "user0"
    assert response['room_id'] == str(room.id)
    await communicator.disconnect()

@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_multitenant_chat_consumer():
    settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
    set_up_data()
    room = Room.objects.create()
    user = get_user_model().objects.get(username="user0")
    room.members.add(user)
    room.save()
    client = Client()
    client.force_login(user=user)
    communicator = WebsocketCommunicator(
        multitenant_application, f"/ws/chat/{room.id}/",
        headers=[
            (
                b'cookie',
                f'sessionid={client.cookies["sessionid"].value}'.encode('ascii')
            ),
            (b'host', b'localhost:8000')]
        )
    connected, subprotocol = await communicator.connect()
    assert connected
    data = {
        'type': 'text',
        'message': "Hello!",
        'sender': user.username,
        'room_id': str(room.id),
        }
    await communicator.send_json_to(data)
    response = await communicator.receive_json_from()
    response = response
    message = Message.objects.all()[0]
    time = message.date_created
    # zone = pytz.timezone(get_default_timezone_name())
    # time = time.astimezone(tz=zone)
    # formatted = dateformat.DateFormat(time)
    # time = formatted.format('M d, Y h:i a')

    assert response['message_type'] == 'text'
    assert response['message'] == 'Hello!'
    assert response['sender'] == 'user0'
    assert response['room_id'] == str(room.id)
    assert response['date_created'] == time.strftime("%d %b %Y %H:%M:%S %Z")
    await communicator.disconnect()

@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_harmful_message_in_chat_consumer():
    settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
    set_up_data()
    room = Room.objects.create()
    user = get_user_model().objects.get(username="user0")
    room.members.add(user)
    room.save()
    client = Client()
    client.force_login(user=user)
    communicator = WebsocketCommunicator(
        application, f"/ws/chat/{room.id}/",
        headers=[
            (
                b'cookie',
                f'sessionid={client.cookies["sessionid"].value}'.encode('ascii')
            ),
            (b'host', b'localhost:8000')]
        )
    connected, subprotocol = await communicator.connect()
    assert connected
    data = {
        'type': 'text',
        'message': "<script>evil();</script>",
        'sender': user.username,
        'room_id': str(room.id),
        }
    await communicator.send_json_to(data)
    response = await communicator.receive_json_from()
    assert response['message'] == "&lt;script&gt;evil();&lt;/script&gt;"
    assert response['sender'] == "user0"
    assert response['room_id'] == str(room.id)
    await communicator.disconnect()
