from django.contrib.auth import get_user_model
from django.urls import reverse, resolve

from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient

from django_chatter.views import IndexView
from django_chatter.models import Room, Message

class TestIndexView(TenantTestCase):

    def setUp(self):
        super().setUp()
        self.client = TenantClient(self.tenant)
        user = get_user_model().objects.create(username="ted")
        user.set_password('dummypassword')
        user.save()

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
        self.assertEqual(response.redirect_chain[0][0], room_url)
        self.assertEqual(str(room.id), response.context['room_uuid_json'])
        self.assertQuerysetEqual(
            response.context['latest_messages'],
            Message.objects.all()
        )
        self.assertEqual(response.context['room_name'], 'Notes to Yourself')
        self.assertTemplateUsed(response, 'django_chatter/base.html')
        self.assertTemplateUsed(response, 'django_chatter/chat-window.html')
        self.assertTemplateUsed(response, 'django_chatter/chatroom-list.html')
        self.assertQuerysetEqual(response.context['rooms_with_unread'], Room.objects.none())
