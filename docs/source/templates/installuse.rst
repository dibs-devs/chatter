Installation and Use
====================

Installing Chatter requires several simple steps. While previous exposure to
`Django Channels <channels.readthedocs.io>`_ would help you, it's not required.

------------
Installation
------------

* Chatter is on `PyPi <https://pypi.org/project/django-chatter/>`_ now! To install it, run

  .. code-block:: python

    pip install django-chatter

  This should install all the required dependencies for Chatter.

* Install `Redis <https://redis.io/download>`_ by following the tutorial there.

* Once you're done with that, add it to your :code:`settings.INSTALLED_APPS`:

  .. code-block:: python

    INSTALLED_APPS = [
      ...
      'chat',
      ...
      ]

* If you haven't already, create a file named :code:`routing.py` in your project's
  configuration folder. This should be the same as the folder where your `settings.py`
  file is located.

  In :code:`routing.py`, add the following lines:

  .. code-block:: python

    from channels.auth import AuthMiddlewareStack
    from channels.routing import ProtocolTypeRouter, URLRouter
    import chat.routing

    application = ProtocolTypeRouter({
      'websocket': AuthMiddlewareStack(
        URLRouter(
        chat.routing.websocket_urlpatterns
        )
      )
    })

  This routes all websocket requests to Chatter, with the logged in :code:`User` object.
  If you are using different `django-channels <https://channels.readthedocs.io/en/latest/>`_
  applications other than Chatter, you may already have this file, and can add the
  appropriate URL for chatter to handle. More details can be found on Django Channels'
  `Routing <https://channels.readthedocs.io/en/latest/topics/routing.html>`_ page.

  If you know how the `middleware wrapping in Channels <https://github.com/django/channels/blob/master/channels/auth.py>`_
  works, then feel free to replace :code:`AuthMiddlewareStack` with what you use
  as your auth middleware for User object processing.

* Link :code:`chat.urls` to the URL you want in your URLConf (:code:`<project config>/urls.py`).

  Example:

  .. code-block:: python

    from django.urls import path, include

    ...
    urlpatterns = [
      ...,
      path('chat/', include('chat.urls')),
      ...
    ]

* Run migrations:

  .. code-block:: bash

    $ python manage.py makeimigrations chat
    $ python manage.py migrate

* Start your app's development server and go to your :code:`'/chat/'` URL,
  and you will see Chatter's homepage.

**Tests haven't been setup for this package yet. I built this app before
I knew what good test practices were like. So, tests welcome!**

-----------
Usage Notes
-----------

* Chatter, as of right now, provides a very minimal interface for users to chat with other users.
  For starters, while group chatting is supported on the model layer,
  the corresponding templates and front-end logic have not yet been setup.

* If you're using chatter as a package in your own app, you have to make sure
  that you handle user authentication in your app. Chatter, by default, provides
  views that require user authentication. If you're developing Chatter on the other
  hand, the usage will vary a bit. The notes for that can be found in the
  :doc:`Get Involved <develop>` section.
