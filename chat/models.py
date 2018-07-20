from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#This model is used to give date and time when a message was created/modified.
class MessagesDateModel(models.Model):
	date_created = models.DateTimeField(auto_now_add = True)
	date_modified = models.DateTimeField(auto_now = True)
	time_modified = models.TimeField(auto_now_add = True)

	class Meta:
		abstract = True

