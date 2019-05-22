from django.test import TestCase
from django_chatter.models import Room, Message
from django.contrib.auth.models import User
from uuid import UUID
from django.db.models import Q, Count
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class RoomTestCase(TestCase):

	def setUp(self):
		user_list = []
		for i in range(3):
			user = get_user_model().objects.create(username=f"user{i}")
			user_list.append(user)
		room = Room.objects.create()
		room.members.add(*user_list)
		self.roomlist = Room.objects.all()

	def validate_uuid(self, uuid_string):
		try:
			val = UUID(uuid_string, version = 4)
			return val
		except ValueError:
			return False

	def test_rooms_have_valid_uuid(self):
		print ('testing if rooms have valid UUIDs.')
		for room in self.roomlist:
			self.assertTrue(self.validate_uuid(str(room.id)))

	def test_rooms_titles(self):
		print ('testing room name of room with three users')
		users = get_user_model().objects.all()
		rooms_with_member_count = Room.objects.annotate(num_members = Count('members'))
		rooms = rooms_with_member_count.filter(num_members = len(users))
		for member in users:
			rooms = rooms.filter(members = member)
		if rooms.exists():
			room = rooms[0]
		self.assertEqual(room.__str__(), "user0, user1, user2")

	def test_invalid_room_id(self):
		print ('testing room creation exception with invalid room id')
		room = Room(id="invaliduuid")
		self.assertRaises(ValidationError, room.save)


class MessageTestCase(TestCase):

	def setUp(self):
		user = get_user_model().objects.create(username="user0")
		room = Room()
		room.save()
		room.members.add(user)
		message = Message(room=room, sender=user, text="Notes to myself")
		message.save()

	def test_message_title(self):
		print('testing message titles')
		self.assertEqual(Message.objects.all()[0].__str__(),
			'Notes to myself sent by "user0" in Room "user0"')
