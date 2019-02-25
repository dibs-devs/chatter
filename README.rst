Django Chatter
==============

Django-based Chat app that supports group chat and real-time updates.
---------------------------------------------------------------------

Full docs here: `Chatter Docs <https://django-chatter.readthedocs.io>`_

Chat is a crucial aspect of many web apps at present.
However, Django's package repository does not have well-maintained reusable chat
packages that Django developers can integrate into their platforms.

Chatter is an attempt to change that. This is an open-source fully reusable chat
application that has mechanisms to support group chats in place.

The default templates for this app are made with Bootstrap, one of the most
popular CSS frameworks out there. This makes it easier for developers to change
the templates just by modifying the right CSS files.

[More work to be done] Added to that, it can also possibly be used as a REST API,
since all the views generate standard JSON responses that need to be parsed by the
websockets present in the front-end of the app using this package.

This app makes use of `Django Channels 2 <http://channels.readthedocs.io>`_ and uses
`Redis <https://redis.io/>`_ as the message broker.

**This app is still in its alpha phase. We plan to improve it so it can be used
as a package in other Django-based web apps. **

To run chatter properly, you'll require `python>=3.5` and Redis. **Note:**
For development, we are currently using `redis-5.0.3`, built from source on
Ubuntu machines.

The core mechanisms of Chatter follows the instructions provided in the
`Django Channels <https://channels.readthedocs.io/en/latest/>`_ tutorial section,
with some added modifications and theming.

------------
Installation
------------

* Chatter is on `PyPi <https://pypi.org/project/django-chatter/>`_ now!
  To install it, run

  .. code-block:: python

    pip install django-chatter

  This should install all the required dependencies for Chatter.

* Once you're done with that, add it to your :code:`settings.INSTALLED_APPS`:

  .. code-block:: python

    INSTALLED_APPS = [
      ...
      'django_chatter',
      ...
      ]

* Since we use Redis as our message broker, you need to enable channel layers
  for Chatter's ChatConsumer
  (see `Channels' Consumers
  <https://channels.readthedocs.io/en/latest/topics/consumers.html>`_
  for more details). To enable that, you need to add the following lines to
  your project's :code:`settings.py` file:

  .. code-block:: python

    CHANNEL_LAYERS = {
      'default': {
          'BACKEND': 'channels_redis.core.RedisChannelLayer',
          'CONFIG': {
              "hosts": [('127.0.0.1', 6379)],
          },
      },
    }

* If you haven't already, create a file named :code:`routing.py` in your
  project's configuration folder.
  This is because Django Channels uses a specification called
  `ASGI <https://channels.readthedocs.io/en/latest/asgi.html>`_
  for its websocket protocol. To enable Channels on your app, you have to add
  a file that routes all websocket requests to a Channels app
  (in this case, Chatter).
  This should be the same as the folder where your :code:`settings.py`
  file is located.

  In :code:`routing.py`, add the following lines:

  .. code-block:: python

    from channels.auth import AuthMiddlewareStack
    from channels.routing import ProtocolTypeRouter, URLRouter
    import django_chatter.routing

    application = ProtocolTypeRouter({
      'websocket': AuthMiddlewareStack(
        URLRouter(
        django_chatter.routing.websocket_urlpatterns # send websocket requests to chatter's urls
        )
      )
    })

  This routes all websocket requests to Chatter, with the logged in :code:`User`
  object. If you are using different
  `django-channels <https://channels.readthedocs.io/en/latest/>`_
  applications other than Chatter, you may already have this file, and can add
  the appropriate URL for chatter to handle.
  More details can be found on Django Channels'
  `Routing <https://channels.readthedocs.io/en/latest/topics/routing.html>`_ page.

  If you know how the middleware wrapping in
  `Channels <https://github.com/django/channels/blob/master/channels/auth.py>`_
  works, then feel free to replace :code:`AuthMiddlewareStack` with what you use
  as your auth middleware for User object processing (if you're curious to know
  about this, get in touch! We'd be happy to talk to you about it).

* Now that you're done setting up :code:`routing.py`, add the following line in
  your :code:`settings.py` file to link to the `routing.py` (again, you may have
  already done this if you're already using channels)

  .. code-block:: python

    ASGI_APPLICATION = '<project name>.routing.application'

* Chatter uses a context processor to generate a list of all rooms that a user
  is a member of. To use this context processor, add it to your :code:`TEMPLATES`
  list in your :code:`settings.py` file:

  .. code-block:: python

    TEMPLATES = [
      {
        ...
        'OPTIONS': {
          'context_processors': [
            ...,
            'django_chatter.context_processors.get_chatroom_list',
            ...,
          ],
        },
      },
    ]

* Link :code:`django_chatter.urls` to the URL you want in your
  URLConf (:code:`<project>/urls.py`).

  Example:

  .. code-block:: python

    from django.urls import path, include

    ...
    urlpatterns = [
      ...,
      path('chat/', include('django_chatter.urls')),
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

* Chatter, as of right now, provides a very minimal interface for users to chat
  with other users.For starters, while group chatting is supported on the model
  layer, the corresponding templates and front-end logic have not yet been setup.

* If you're using chatter as a package in your own app, you have to make sure
  that you handle user authentication in your app. Chatter, by default, provides
  views that require user authentication. If you're developing Chatter on the other
  hand, the usage will vary a bit. The notes for that can be found in the
  `Get Involved <https://django-chatter.readthedocs.io/en/latest/templates/develop.html>`_
  section.

-------------------------------
Running list of features to add
-------------------------------

* Add a "Create Group" option for users on the templates
* Add 'Seen by user x' functionality
* Add displaying time with messages
