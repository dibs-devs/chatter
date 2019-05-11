Welcome to Django Chatter's documentation!
==========================================


**Django-based Chat app that supports group chat and real-time updates.**

Chat is a crucial aspect of many web apps at present. However, Django's package
repository does not have well-maintained reusable chat packages that Django
developers can integrate into their platforms.

Django Chatter is an attempt to change that. This is an open-source fully reusable
chat application that has mechanisms to support group chats in place.

the HTML front-end for this app is built with Flexbox, making it responsive to
numerous viewports. 

[More work to be done] Added to that, it can also possibly be used as a REST API,
since all the views generate standard JSON responses that need to be parsed by
the websockets present in the front-end of the app using this package.

This app makes use of `Django Channels 2 <http://channels.readthedocs.io>`_ and uses
`Redis <https://redis.io/>`_ as the message broker.

To run chatter properly, you'll require :code:`python>=3.5` and Redis.
**Note:** For development, we are currently using :code:`redis-5.0.3`,
built from source on Ubuntu machines.

The core mechanisms of Chatter follows the instructions provided in the
`Django Channels Tutorial <https://channels.readthedocs.io/en/latest/tutorial/index.html>`_
section, with some added modifications and a little theming.

**This app is still in its alpha phase.We plan to improve it so
it can be used as a package in other Django-based web apps.**


Contents
--------
.. toctree::
   :maxdepth: 2

   templates/installuse
   templates/examples
   templates/customize
   templates/utilities
   templates/test
   templates/develop
   templates/credits
