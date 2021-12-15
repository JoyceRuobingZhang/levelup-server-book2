from django.db import models
from django.db.models.deletion import CASCADE
from .gamer import Gamer
from .gametype import Gametype

class Game(models.Model):
    
    name = models.CharField(max_length=55)
    player_limit = models.IntegerField()
    created_by = models.ForeignKey(Gamer, on_delete=CASCADE, related_name='created_by')
    gametype = models.ForeignKey(Gametype, on_delete=CASCADE, related_name='gametype')
    