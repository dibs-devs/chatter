from django.test import TestCase
from django_chatter.models import Room, Message
from django.contrib.auth.models import User
from uuid import UUID
from django.db.models import Q, Count
from django.contrib.auth import get_user_model

class RoomTestCase(TestCase):
	'''
	AI-------------------------------------------------------------------
		The test database contains:
			a) Three distinct Users
			b) Three distinct Rooms
			c) The Rooms have 1,2 and 3 users each.
	-------------------------------------------------------------------AI
	'''
	fixtures = ['database_dump.json']

	def setUp(self):
		self.new_room = Room()
		self.new_room.save()
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
		self.assertEqual(room.__str__(), "aishtiaque, lol, hello")


class MessageTestCase(TestCase):
	'''
	AI-------------------------------------------------------------------
		The test database contains:
			a) Three distinct Users
			b) Three distinct Rooms
			c) The Rooms have 1,2 and 3 users each.
	-------------------------------------------------------------------AI
	'''
	fixtures = ['database_dump.json']

	def test_message_title(self):
		print('testing message titles')
		self.assertEqual(Message.objects.all()[0].__str__(),
			'hey sent by "lol" in Room "lol"')
