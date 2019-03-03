from channels.auth import AuthMiddleware
from channels.sessions import CookieMiddleware, SessionMiddleware
from channels.db import database_sync_to_async

from django.contrib.sessions.models import Session
from django.utils.crypto import constant_time_compare
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import (
    get_user_model,
    HASH_SESSION_KEY,
    SESSION_KEY,
)
from django.db.models import Count

from django_chatter.models import Room

# custom get_user method for AuthMiddleware subclass. Mostly similar to
# https://github.com/django/channels/blob/master/channels/auth.py
@database_sync_to_async
def get_user(scope):
    """
    Return the user model instance associated with the given scope.
    If no user is retrieved, return an instance of `AnonymousUser`.
    """
    if "session" not in scope:
        raise ValueError(
            "Cannot find session in scope.\
            You should wrap your consumer in SessionMiddleware."
        )
    session_key = scope['cookies']['sessionid']
    for key, value in scope.get('headers', []):
        if key == b'host':
            schema_name = value.decode('ascii').split('.')[0]
    user = None
    try:
        # get session and user using django-tenants' schema_context
        #  Link: https://django-tenants.readthedocs.io/en/latest/use.html#utils
        from django_tenants.utils import schema_context
        with schema_context(schema_name):
            session = Session.objects.get(session_key=session_key)
            uid = session.get_decoded().get(SESSION_KEY)
            user = get_user_model().objects.get(pk=uid)

            # Verifying the session
            # collected from:
            # https://github.com/django/channels/blob/master/channels/auth.py
            # line 44 onwards
            if hasattr(user, "get_session_auth_hash"):
                session_hash = session.get(HASH_SESSION_KEY)
                session_hash_verified = session_hash and constant_time_compare(
                    session_hash, user.get_session_auth_hash()
                )
                if not session_hash_verified:
                    session.flush()
                    user = None
    except Exception as e:
        pass
    return user or AnonymousUser()


# Auth Middleware that attaches users to websocket scope on multitenant envs.
class MTAuthMiddleware(AuthMiddleware):
    async def resolve_scope(self, scope):
        scope["user"]._wrapped = await get_user(scope)


# Adds the schema name to scope and passes it down the stack of middleware ASGI apps.
# Adds a boolean as well indicating whether it's a multitenant environment or not.
class MTSchemaMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        if "headers" not in scope:
            raise ValueError(
                "MTSchemaMiddleware was passed a scope that did not have a headers key "
                + "(make sure it is only passed HTTP or WebSocket connections)"
            )

        for key, value in scope.get('headers', []):
            if key == b'host':
                schema_name = value.decode('ascii').split('.')[0]
                break
        else:
            raise ValueError(
                "The headers key in the scope is invalid. "
                + "(make sure it is passed valid HTTP or WebSocket connections)"
            )
        return self.inner(
            dict(scope, schema_name=schema_name, multitenant=True)
        )


# MiddlewareStack to give access to user object in a multitenant environment
ChatterMTMiddlewareStack = lambda inner: CookieMiddleware(
    SessionMiddleware(
        MTSchemaMiddleware(
            MTAuthMiddleware(inner)
        )
    )
)


# Takes in a list of User objects and returns the UUID of the room created.
def create_room(user_list):
    for user in user_list:
        if type(user) != get_user_model():
            raise TypeError("Parameters passed to create_room doesn't " +
                "match your project's user model. Please make sure the list " +
                "you passed contains valid settings.AUTH_USER_MODEL objects.")
    rooms_with_member_count = Room.objects.annotate(num_members = Count('members'))
    rooms = rooms_with_member_count.filter(num_members = len(user_list))

    for member in user_list:
        rooms = rooms.filter(members = member)
    if rooms.exists():
        room = rooms[0]
        return room.id
    else:
        room = Room()
        room.save()
        room.members.set(user_list)
        room.save()
        return room.id
