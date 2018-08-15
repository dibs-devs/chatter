from channels.routing import ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
from channels.sessions import SessionMiddlewareStack

application = ProtocolTypeRouter({
	'websocket': AuthMiddlewareStack(
		URLRouter(
			chat.routing.websocket_urlpatterns
			)
		)
})