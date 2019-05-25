from django.contrib.auth import get_user_model
from django.urls import reverse, resolve

from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient

from django_chatter.views import IndexView, users_list
from django_chatter.models import Room, Message

import json


class TestIndexView(TenantTestCase):

    def setUp(self):
        super().setUp()
        self.client = TenantClient(self.tenant)
        user = get_user_model().objects.create(username="ted")
        user.set_password('dummypassword')
        user.save()
        room = Room.objects.create()
        room.members.add(user)
        message_1 = Message.objects.create(
                                        sender=user,
                                        text="first message",
                                        room=room
                                        )
        message_2 = Message.objects.create(
                                        sender=user,
                                        text="last message",
                                        room=room
                                        )


    def test_chat_render_view(self):
        logged_in = self.client.login(username="ted", password="dummypassword")
        found = resolve(reverse('django_chatter:index'))
        self.assertEqual(
            type(found.func), type(IndexView.as_view())
        )
        response = self.client.get(reverse('django_chatter:index'), follow=True)
        self.assertEqual(response.status_code, 200)
        room = Room.objects.all()[0]
        room_url = f"/chat/{room.id}/"
        message = Message.objects.all()[0]

        self.assertEqual(response.redirect_chain[0][0], room_url)

        self.assertEqual(str(room.id), response.context['room_uuid_json'])

        self.assertEqual(
            response.context['last_messages_in_rooms'],
            [Message.objects.all()[0]]
        )
        self.assertEqual(
            str(response.context['latest_messages_curr_room']),
            str(Message.objects.all())
        )
        self.assertEqual(response.context['room_name'], 'Notes to Yourself')
        self.assertTemplateUsed(response, 'django_chatter/base.html')
        self.assertTemplateUsed(response, 'django_chatter/chat-window.html')
        self.assertTemplateUsed(response, 'django_chatter/chatroom-list.html')

        self.assertQuerysetEqual(
            response.context['rooms_with_unread'],
            Room.objects.none()
        )


class TestUsernames(TenantTestCase):

    def setUp(self):
        super().setUp()
        self.client = TenantClient(self.tenant)
        for i in range(5):
            user = get_user_model().objects.create(username=f"user{i}")
            user.set_password("dummypassword")
            user.save()

    def test_users_list_view(self):
        logged_in = self.client.login(username="user0", password="dummypassword")
        found = resolve(reverse('django_chatter:users_list'))
        self.assertEqual(found.func, users_list)
        response = self.client.get(
            reverse('django_chatter:users_list'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        json_array = []
        for user in get_user_model().objects.all():
            dict = {}
            dict["id"] = user.pk
            dict["text"] = user.username
            json_array.append(dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.content, encoding='utf-8'), json.dumps(json_array))
