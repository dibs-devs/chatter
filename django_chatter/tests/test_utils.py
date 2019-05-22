from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from django_chatter.models import Room
from django_chatter.utils import create_room

from django.conf import settings
from channels.testing import WebsocketCommunicator

from chatter.routing import application, multitenant_application

import json
import pytest

from functional_tests.data_setup_for_tests import set_up_data

class saveRoomTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="user1", password="chatter12345")
        user2 = User.objects.create(username="user2", password="chatter12345")
        user3 = User.objects.create(username="user3", password="chatter12345")

    def test_create_room_with_valid_input(self):
        user1 = User.objects.get(username="user1")
        user2 = User.objects.get(username="user2")
        user3 = User.objects.get(username="user3")
        room_id = create_room([user1, user2, user3])
        room_in_db = Room.objects.all()[0]
        self.assertEqual(room_in_db.id, room_id)

    def test_create_room_with_invalid_input(self):
        self.assertRaises(TypeError, lambda: create_room([1,2,3]))
        self.assertRaises(TypeError, lambda: create_room(['1', '2', '2']))

    def test_create_room_with_empty_input(self):
        self.assertRaises(TypeError, lambda: create_room())

    def test_creating_existing_room(self):
        user1 = User.objects.get(username="user1")
        user2 = User.objects.get(username="user2")
        room_id = create_room([user1, user2])
        new_room_id = create_room([user1, user2])
        self.assertEqual(new_room_id, room_id)


TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_no_host_in_headers():
    settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
    room = Room.objects.create()
    user = get_user_model().objects.create(username="user0")
    room.members.add(user)
    room.save()
    client = Client()
    client.force_login(user=user)
    with pytest.raises(ValueError):
        communicator = WebsocketCommunicator(
            multitenant_application, f"/ws/chat/{room.id}/",
            )

@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_no_session_id_in_headers():
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
        headers = [(b'host', b'localhost:8000')]
        )
    with pytest.raises(KeyError):
        connected, subprotocol = await communicator.connect()
