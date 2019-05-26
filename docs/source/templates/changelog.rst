Changelog
=========

v 1.0.2
-------
- On click, messages show when they were sent.
- Fresh UI, inspired by Google's Messages Web and Facebook Messenger.
- ChatConsumer now sends and receives JSON data by default.
- More modern dropdown for selecting users. This has been put in place to
  allow group chat formation in the future.
- Infinite scroll to retrieve previous messages has been implemented.

v 1.0.1
-------
- Cleaned up some testing code
- Bugfix in MTSchemaMiddleware - hostname to search tenant with was only
  the first part of the domain instead of the whole domain.

v 1.0.0
-------
- This version removes the context processor :code:`get_chatroom_list` that used to fetch a list of all rooms a
  logged in user is a member of. This is to prevent unnecessary database access in the
  request-response cycle. For users using django_chatter < 1.0.0, this will create
  compatibility issues, which can be solved by simply removing the context processor
  from their settings.
- Multiple tests have been added to maintain reliability of the code.
- On multitenant systems, :code:`MTSchemaMiddleware` checks if a tenant with the given
  schema name exists. If not, it raises an Http404 error.

v 0.2.2
-------
- Added testing framework for multitenancy support
- Switched to class-based views to promote clearer code style
- index page `bugfix <https://github.com/dibs-devs/chatter/issues/4>`_
- Added coverage and Travis CI information
