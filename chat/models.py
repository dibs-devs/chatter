from django.db import models
from django.contrib.auth.models import User


# This model is used to give date and time when a message was created/modified.
class DateTimeModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Room(DateTimeModel):
    title = models.CharField(max_length=20, blank=True)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name="creator")
    users = models.ManyToManyField(User, related_name="users")

    @property
    def is_private(self):
        return self.users.objects.count() == 1


class Message(DateTimeModel):
	room = models.ForeignKey(Room, on_delete=models.PROTECT)
	sender = models.ForeignKey(User, on_delete=models.PROTECT)
	content = models.TextField()
