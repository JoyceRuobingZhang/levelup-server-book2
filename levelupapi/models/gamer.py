from django.db import models
from django.contrib.auth.models import User


class Gamer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50)
    signed_up_events = models.ManyToManyField('levelupapi.Event', related_name='signed_up_by') # attendees