from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserMessage(models.Model):
	message = models.ForeignKey(User, on_delete = models.PROTECT)