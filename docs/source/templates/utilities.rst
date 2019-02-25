Utilities
=========

Available
---------

Chatter has the following utilities available:

* **Middleware to Support Multitenancy**

  *Added in: Chatter 0.1.0*
  
  Django Chatter now supports multitenant SaaS applications made using
  `django-tenants <https://github.com/tomturner/django-tenants>`_.
  This is made available as middlewares in the :code:`utils.py` module.
  Both these middlwares require `CookieMiddleware` and `SessionMiddleware` stacked
  higher in the ASGI application routing stack.

  *MTSchemaMiddleware*:

  This middleware attaches :code:`schema_name` as well as a boolean named
  :code:`multitenant` into a websocket consumer's :code:`scope`. This enables
  you to access the schema name from any consumer that's wrapped inside this
  middleware. To do this, you have to add it into your middleware stack in your
  project's `routing.py` file like so:

  .. code-block:: python

    from django_chatter.utils import MTSchemaMiddleware

    application = ProtocolTypeRouter({
    	'websocket': <your stack>(
        MTSchemaMiddleware(
      		URLRouter(
      			django_chatter.routing.websocket_urlpatterns
      			)
      		)
        )
    })

  After doing this, your consumers will have access to the schema_name that you
  can use with `django-tenant`'s `schema_context`.

  *MTAuthMiddleware*:

  This middleware is Chatter's version of attaching a user object to a
  websocket's :code:`scope`. This automatically attaches the logged in user's
  information from the client's session cookies depending on which tenant
  they're accessing Chatter from. You can use it in your project's
  :code:`routing.py` by the following method:

  .. code-block:: python

    from django_chatter.utils import MTAuthMiddleware

    application = ProtocolTypeRouter({
    	'websocket': <your stack>(
        MTAuthMiddleware(
      		URLRouter(
      			django_chatter.routing.websocket_urlpatterns
      			)
      		)
        )
    })

  There's a high chance that you'd want to be using both these middlewares. To
  make things easy, these two are combined with :code:`CookieMiddleware` and
  :code:`SessionMiddleware` to make :code:`ChatterMTMiddlewareStack` which you
  can use like this:

  .. code-block:: python

    from django_chatter.utils import ChatterMTMiddlewareStack

    application = ProtocolTypeRouter({
    	'websocket': <your stack>(
        ChatterMTMiddlewareStack(
      		URLRouter(
      			django_chatter.routing.websocket_urlpatterns
      			)
      		)
        )
    })

To Do
-----

Some utilities would be nice to have integrated with Chatter.
For example, we could have the following:

* A module that takes in a list of :code:`User` objects and creates
  a room with them in it, and returns the UUID of the new Room.
