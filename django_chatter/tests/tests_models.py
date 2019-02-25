from django.test import TestCase
from chat.models import *
from django.contrib.auth.models import User
from uuid import UUID
from django.db.models import Q, Count

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

	# def test_room_member_not_incomplete(self):
