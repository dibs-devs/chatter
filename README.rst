# Chatter

#### Django-based Chat app that supports group chat and real-time updates.

 Chat is a crucial aspect of many web apps at present. However, Django's package repository does not have well-maintained reusable chat packages that Django developers can integrate into their platforms.

 Chatter is an attempt to change that. This is an open-source fully reusable chat application that has mechanisms to support group chats in place.

  The default templates for this app are made with Bootstrap, one of the most popular CSS frameworks out there. This makes it easier for developers to change the templates just by modifying the right CSS files.

 [More work to be done] Added to that, it can also possibly be used as a REST API, since all the views generate standard JSON responses that need to be parsed by the websockets present in the front-end of the app using this package.

This app makes use of [Django Channels 2](http://channels.readthedocs.io) and uses
[Redis](https://redis.io/) as the message broker.

**This app is still in its alpha phase. We plan to improve it so it can be used as a package in other Django-based web apps. **

To run chatter properly, you'll require `python>=3.5` and Redis. **Note:** For development, we are currently using `redis-5.0.3`, built from source on Ubuntu machines.

The core mechanisms of Chatter follows the instructions provided in the [Django Channels](https://channels.readthedocs.io/en/latest/) tutorial section, with some added modifications and theming.

### Integrating Chatter into your project

* Chatter is on [PyPi](https://pypi.org/project/django-chatter/) now! To install it, run

  ```python
  pip install django-chatter
  ```
  This should install all the required dependencies for Chatter.

* Once you're done with that, add it to your `settings.INSTALLED_APPS`:
```python
INSTALLED_APPS = [
...
'chat',
...
]
```

* If you haven't already, create a file named `routing.py` in your project's configuration folder. This should be the same as the folder where your `settings.py` file is located.

  In `routing.py`, add the following lines:

  ```python
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
  ```

  This routes all websocket requests to Chatter, with information about the user who's logged in. If you are using different [django-channels](https://channels.readthedocs.io/en/latest/) applications with chatter, you may already have this file, and can add the appropriate URL for chatter to handle. More details can be found on Django Channels' [Routing](https://channels.readthedocs.io/en/latest/topics/routing.html) page.

  If you know how the middleware wrapping works, then feel free to replace `AuthMiddlewareStack` with what you user as the auth middleware.

* Link `chat.urls` to the URL you want in your URLConf (`<project config>/urls.py`). Example:
  ```python
  from django.urls import path, include

  ...
  urlpatterns = [
    ...,
    path('chat/', include('chat.urls')),
    ...
  ]
  ```
* Run migrations:
`python manage.py makeimigrations chat`

  `python manage.py migrate`
* Start your app's development server and go to your `'/chat/'` URL, and you will see Chatter's homepage.

**Tests haven't been setup for this package yet. I built this app before
I knew what good test practices were like. So, tests welcome!**

### Usage Notes

* Chatter, as of right now, provides a very minimal interface for users to chat with other users.
For starters, while group chatting is supported on a database level,
the corresponding templates and front-end logic have not yet been setup.
* If you're using chatter as a package in your own app, you have to make sure
to handle user authentication in your app. Chatter, by default, provides
views that require user authentication. If you're developing Chatter on the other
hand, the usage will vary a bit. The notes for that can be found in the Contributing
section.


### Running list of features to add

* Add a "Create Group" option for users on the templates
* Notifications using django-notifications
* Add 'Seen by user x' functionality
* Multitenancy support in conjuction with [django-tenants](https://www.github.com/tomturner/django-tenants)
