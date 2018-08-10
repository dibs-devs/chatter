import uuid

from django.db import models
from django.contrib.auth.models import User



# This model is used to give date and time when a message was created/modified.
class DateTimeModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Room(DateTimeModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
            editable=False
        )
    members = models.ManyToManyField(User)

    def __str__(self):
        room = Room.objects.get(id=self.id)
        memberset = room.members.all()
        members_list = []
        for member in memberset:
            members_list.append(member.username)

        return str(members_list)

class Message(DateTimeModel):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return '"{}" \
        sent by "{}" \
        in Room "{}"'.format(
                        self.text,
                        self.sender,
                        self.room
                    )
