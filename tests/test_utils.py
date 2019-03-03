from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from django_chatter.models import Room
from django_chatter.utils import create_room

class saveRoomTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="user1", password="chatter12345")
        user2 = User.objects.create(username="user2", password="chatter12345")
        user3 = User.objects.create(username="user3", password="chatter12345")

    def test_create_room_with_valid_input(self):
        user1 = User.objects.get(username="user1")
        user2 = User.objects.get(username="user2")
        user3 = User.objects.get(username="user3")
        try:
            room_id = create_room([user1, user2, user3])
            room_in_db = Room.objects.all()[0]
            self.assertEqual(room_in_db.id, room_id)
        except TypeError as e:
            raise e
            self.fail()

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
