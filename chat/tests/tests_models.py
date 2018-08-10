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

class RoomMemberTestCase(TestCase):
	fixtures = ['database_dump.json']

	def setUp(self):
		# Variables used in RoomMember initialization tests
		self.new_room = Room()
		self.new_room.save()
		self.new_user = User(username = 'sample1')
		self.new_user.save()
		self.new_member = RoomMember()
		self.existing_user = User.objects.get(username='superuser')
		
		'''
		AI-------------------------------------------------------------------
			Variables to get a Room that contains two users, one of whom
			is kruto. To get a room that contains 
		-------------------------------------------------------------------AI
		'''
		'''
		kruto = User.objects.get(username = 'kruto')

		#Annotate adds the num_members variable to every Room object
		#and the number is equal to the number of members in that Room object.
		rooms_with_member_count = Room.objects.annotate(num_members = Count('members'))

		#Returns a QuerySet of Rooms that have Ken in them
		rooms_with_ken = rooms_with_member_count.filter(members=kruto)
		#Returns a QuerySet of Rooms with Ken that have two members
		room_with_ken_and_other = rooms_with_ken.filter(num_members__gte=2).filter(num_members__lte=2)
		'''

	# Checks if the save() method works i.e. invalid or valid RoomMembers
	#are saved to database
	def save_room_member(self):
		try:
			self.new_member.save()
			test_passed = True
		except Exception as ex:
			print ('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
			template = 'An exception of type {} occured. Arguments: \n{}'
			message = template.format(type(ex).__name__, ex.args)
			print (message)
			print ('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
			test_passed = False
		return test_passed

	'''
	AI-------------------------------------------------------------------
		RoomMember initialization tests. These tests try to save invalid
		rooms and checks for appropriate errors and then saves a valid
		room to see if it's saved.
	-------------------------------------------------------------------AI
	'''
	def test_room_member_not_empty(self):
		print ('\n---------------------------------------------------------------')
		print ('Checking that empty RoomMember can\'t be saved to database.')
		test_passed = self.save_room_member()
		print ('---------------------------------------------------------------')
		self.assertFalse(test_passed)

	def test_room_member_no_user(self):
		print ('\n---------------------------------------------------------------')
		print ('Testing if RoomMember saves if it doesn\'t have a user.\n')
		self.new_member.room = self.new_room
		test_passed = self.save_room_member()
		print ('---------------------------------------------------------------')
		self.assertFalse(test_passed)

	def test_room_member_no_room(self):
		print ('\n---------------------------------------------------------------')
		print ('Testing if RoomMember saves if it doesn\'t have a room.')
		self.new_member.user = self.new_user
		test_passed = self.save_room_member()
		print ('---------------------------------------------------------------')
		self.assertFalse(test_passed)

	def test_complete_room_member(self):
		print ('\n---------------------------------------------------------------')
		print ('Testing if RoomMember saves with everything in it.')
		self.new_member.user = self.new_user
		self.new_member.room = self.new_room
		test_passed = self.save_room_member()
		print ('---------------------------------------------------------------')
		self.assertTrue(test_passed)


'''
class MessageTestCase(TestCase):
	def setUp(self):
		

'''
