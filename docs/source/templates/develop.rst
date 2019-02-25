Get Involved with Django Chatter!
=================================

We'd highly appreciate contributions to this project! The source code is currently
hosted on `GitHub <https://www.github.com/dibs-devs/chatter>`_. If you caught a
bug or have suggestions, we welcome pull requests and issues!

Currently, `Ahmed Ishtiaque <https://ishtiaque06.github.io>`_ is the primary maintainer
for this project. If you have any questions or suggestions, feel free to
reach out to him as well.

Get Started
-----------

To start developing Chatter, follow the following steps:

* Install `Python 3 <https://www.python.org/>`_ if you don't have it already.
* Clone the `GitHub Repo <https://github.com/dibs-devs/chatter>`_.
* Spawn up a new virtual environment, :code:`cd` into your working directory
  and run

  .. code-block:: bash

    $ pip install -r dev-requirements.txt

  This will install all the prerequisites needed to run Chatter.
* If you don't have Redis, you can install it from
  `their Download page <https://redis.io/download>`_.

* Since we're phasing into implementing multitenancy support on Chatter with
  `django-tenants <https://www.github.com/tomturner/django-tenants>`_, we will
  be using PostgreSQL as the database. Install PostgreSQL from
  `PostgreSQL <https://www.postgresql.org/>`_.

  After this, create user for chatter database:

  * Open the postgres terminal:

    .. code-block:: bash

      $ sudo su - postgres

  * Connect to your psql server:

    .. code-block:: bash

      $ psql

  * Run the following commands (don't miss the semi-colons):

    .. code-block:: bash

      # CREATE DATABASE chatter;
      # CREATE USER chatteradmin WITH PASSWORD 'chatter';
      # ALTER ROLE chatteradmin SET client_encoding TO 'utf8';
      # ALTER ROLE chatteradmin SET default_transaction_isolation TO 'read committed';
      # ALTER ROLE chatteradmin SET timezone TO 'America/New_York';
      # GRANT ALL PRIVILEGES ON DATABASE chatter TO chatteradmin;
      # \q

    The instructions should be pretty intuitive. This is a replication of the
    detailed PostgreSQL install guide on
    `DigitalOcean <https://www.digitalocean.com/
    community/tutorials/how-to-use-postgresql-with-your-django-application
    -on-ubuntu-14-04>`_.

  * Exit the postgres session:

    .. code-block:: bash

      $ exit

* Run migrations:

  .. code-block:: bash

    $ python manage.py makemigrations django_chatter
    $ python manage.py migrate

* Create a superuser for chatter:

  .. code-block:: bash

    $ python manage.py createsuperuser

* Run the development server:

  .. code-block:: bash

    $ python manage.py runserver

* (Optional) if you want to streamline the login/logout mechanisms, feel free to
  add a :code:`login.html` file to `django_chatter/templates/registration` folder. This
  should give you a form to log in. Django's
  `template <https://docs.djangoproject.com/
  en/2.1/topics/auth/default/#django.contrib.auth.views.LoginView>`_
  for that is pretty adequate.

The following is a list of features and hooks that we plan on bringing to Chatter:

Features Yet to Come
--------------------
* Add a "Create Group" option for users on the templates
* Add 'Seen by user x' functionality
* Add time to when messages were sent
