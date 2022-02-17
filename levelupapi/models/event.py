from django.db import models
from django.db.models.deletion import CASCADE
from .gamer import Gamer
from .game import Game
from .status import Status



class Event(models.Model):
    
    name = models.CharField(max_length=55)
    time = models.DateTimeField()
    status = models.ForeignKey(Status, on_delete=CASCADE, related_name='events') # default=1
        #under the hood: status_id = ..; one-to-many relations (show on the one side, not the many side)
    host = models.ForeignKey(Gamer, on_delete=CASCADE, related_name='hosting_events') # alias event_set
    game = models.ForeignKey(Game, on_delete=CASCADE, related_name='events')
    
    # for custom properties that are not stored in the database
    @property
    def joined(self):
        return self.__joined
    
    @joined.setter
    def joined(self, value):
        self.__joined = value
        
        

    
    
   