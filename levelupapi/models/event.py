from django.db import models
from django.db.models.deletion import CASCADE
from .gamer import Gamer
from .game import Game
from .status import Status



class Event(models.Model):
    
    name = models.CharField(max_length=55)
    time = models.DateTimeField()
    status = models.ForeignKey(Status, on_delete=CASCADE, related_name='status')
    host = models.ForeignKey(Gamer, on_delete=CASCADE, related_name='hosts')
    game = models.ForeignKey(Game, on_delete=CASCADE, related_name='games')
    
    