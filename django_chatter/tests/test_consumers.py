from channels.testing import WebsocketCommunicator
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.layers import get_channel_layer

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

def prepare_room_and_user():
    set_up_data()
    room = Room.objects.create()
    user = get_user_model().objects.get(username="user0")
    room.members.add(user)
    room.save()
    client = Client()
    client.force_login(user=user)
    return client, room, user

@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_single_tenant_chat_consumer():
    settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
    client, room, user = prepare_room_and_user()
    communicator = WebsocketCommunicator(
        application, f"/ws/django_chatter/chatrooms/{room.id}/",
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
        'message_type': 'text',
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
    client, room, user = prepare_room_and_user()
    communicator = WebsocketCommunicator(
        multitenant_application, f"/ws/django_chatter/chatrooms/{room.id}/",
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
        'message_type': 'text',
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
    client, room, user = prepare_room_and_user()
    communicator = WebsocketCommunicator(
        application, f"/ws/django_chatter/chatrooms/{room.id}/",
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
        'message_type': 'text',
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

@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_chat_alert_consumer():
    settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
    client, room, user = prepare_room_and_user()
    user1 = get_user_model().objects.get(username="user1")
    other_client = Client()
    other_client.force_login(user=user1)
    room_with_two = Room.objects.create()
    room_with_two.members.add(*[user, user1])
    room_with_two.save()
    room_with_user_1 = Room.objects.create()
    room_with_user_1.members.add(user1)
    room_with_user_1.save()

    chat_communicator = WebsocketCommunicator(
        application, f"/ws/django_chatter/chatrooms/{room_with_two.id}/",
        headers=[
            (
                b'cookie',
                f'sessionid={client.cookies["sessionid"].value}'.encode('ascii')
            ),
            (b'host', b'localhost:8000')]
        )
    connected, subprotocol = await chat_communicator.connect()
    assert connected

    user1_alert_communicator = WebsocketCommunicator(
        application, f"/ws/django_chatter/users/{user1.username}/",
        headers=[
            (
                b'cookie',
                f'sessionid={other_client.cookies["sessionid"].value}'.encode('ascii')
            ),
            (b'host', b'localhost:8000')]
    )
    connected, subprotocol = await user1_alert_communicator.connect()
    assert connected

    data = {
        'message_type': 'text',
        'message': "<script>evil();</script>",
        'sender': user.username,
        'room_id': str(room_with_two.id),
        }
    await chat_communicator.send_json_to(data)
    response = await chat_communicator.receive_json_from()
    alert = await user1_alert_communicator.receive_json_from()
    assert response['message'] == "&lt;script&gt;evil();&lt;/script&gt;"
    assert response['sender'] == "user0"
    assert response['room_id'] == str(room_with_two.id)
    await chat_communicator.disconnect()


    assert alert['message'] == "&lt;script&gt;evil();&lt;/script&gt;"
    assert alert['sender'] == "user0"
    assert alert['room_id'] == str(room_with_two.id)
    await user1_alert_communicator.disconnect()
