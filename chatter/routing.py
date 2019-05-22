from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import django_chatter.routing
from django_chatter.utils import ChatterMTMiddlewareStack

application = ProtocolTypeRouter({
	'websocket': AuthMiddlewareStack(
		URLRouter(
			django_chatter.routing.websocket_urlpatterns
			)
		)
})

multitenant_application = ProtocolTypeRouter({
	'websocket': ChatterMTMiddlewareStack(
		URLRouter(
			django_chatter.routing.websocket_urlpatterns
			)
		)
})
