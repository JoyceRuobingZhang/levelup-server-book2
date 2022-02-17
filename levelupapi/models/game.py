from django.db import models
from django.db.models.deletion import CASCADE
from .gamer import Gamer
from .gametype import Gametype

class Game(models.Model):
    
    name = models.CharField(max_length=55)
    # max_length: to know how much space in memory should give to the row
    player_limit = models.IntegerField()
    created_by = models.ForeignKey(Gamer, on_delete=CASCADE, related_name='created_by')
    gametype = models.ForeignKey(Gametype, on_delete=CASCADE, related_name='gametype')
    
    
    #🕹🕹🕹Events per Game with Django
        
    #Since the event count is a calculated property, and not something stored in the database, 
    #create a custom property that will be added to each instance of a Game：
    @property
    def event_count(self):
        return self.__event_count

    @event_count.setter
    def event_count(self, value):
        self.__event_count = value