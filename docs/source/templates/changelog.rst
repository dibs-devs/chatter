Changelog
=========

v 1.0.7
-------
- Bugfix: Properly selecting the last 10 rooms when loading a chat window.

v 1.0.6
-------
- UI improvement: the Opponent username bubble has alignment flex-end to ensure it's in the bottom
- Cache usernames of all users present in a room to save database queries


v 1.0.5
-------
- Major change: Now, whenever a user/client connects to a room, the UI gets updated
  if they receive messages in a separate room. This is achieved by connecting to
  an additional websocket that is defined by the user's username. New alerts are
  received in this websocket and the update is added to the UI.
- Tests are added to test this new websocket consumer's behavior.
- Refactored more of the JS code into their own files and added the dependencies
  on the top of each file.
- Minor UI improvements to keep things intuitive


v 1.0.4
-------
- Bugfixes: The last message preview on chatroom-list updates as the websocket
  receives new messages. Overflow of text in the preview has been adjusted for.

v 1.0.3
-------
- Minor bugfix: Use relative URL when fetching messages to account for parent
  app's URL settings.

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
