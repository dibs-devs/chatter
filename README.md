# Chatter

#### Django-based Chat app that supports group chat and real-time updates.

This app makes use of [Django Channels 2](http://channels.readthedocs.io) and uses
[Redis](https://redis.io/) as the message broker. 

###### This app is still in its alpha phase. We plan to improve it so it can be used as a package in other Django-based web apps.  

**Community support and ideas for improvement most welcome!**

#### Python dependency: Python 3.5

#### The app needs Redis server to be running in the background to function properly.
#### Since Redis is natively available only for Unix systems, we can't support Windows.  

# Installation and first use

* Clone this repository: [https://github.com/dibs-devs/chatter.git]
* Install required packages: `pip install -r requirements.txt`
* Install Redis: [https://redis.io]
* Run migrations: `python manage.py makemigrations chat && python manage.py migrate`
* Create superuser for initial setup: `python manage.py createsuperuser`
* Fire up Redis server: `redis-server` 
  (this app is configured to communicate at 6379, the default
  port for Redis) **important**
* Run the development server: `python manage.py runserver`
* Go to `localhost:8000/admin` in a browser
* Log in using the newly created superuser
* Create as many more users as you want
* Create rooms in which users can chat
* Go to `localhost:8000` 
* Start chatting!


**Unit tests haven't been setup for this package yet. Tests welcome!**


# Running list of features to add

* Add a "Create Group" option
* Notifications using django-notifications
* Improve 'Seen by user x' functionality

