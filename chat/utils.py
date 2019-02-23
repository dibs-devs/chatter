from channels.auth import AuthMiddleware

# Auth Middleware that attaches users to websocket scope on multitenant envs.
class ChatterMTAuthMiddleware(AuthMiddleware):
    pass
