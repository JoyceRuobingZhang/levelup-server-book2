"""View module for handling requests about park areas"""
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from levelupapi.models import Event, Gamer, Game


# BEND THE RULE: The ❗️list() method isn't going to return a list of anything, but rather ❗️a single thing. 
# You are going to expose a URL (http://localhost:8000/profile) in your Django app that will return the profile information
# for a single user, ❗️without the need for a route parameter of the user's id. 
# Instead, the Authorization header (the token) will be used to identify the user. 

class ProfileView(ViewSet):
    """Gamer can see profile information"""

    def list(self, request):
        """Handle GET requests to profile resource

        Returns:
            Response -- JSON representation of user info and events
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        events = Event.objects.filter(signed_up_by=gamer)

        events = EventSerializer(
            events, many=True, context={'request': request})
        gamer = GamerSerializer(
            gamer, many=False, context={'request': request})

        # Manually construct the JSON structure you want in the response
        # There are two keys on the response object: 
        # gamer - {an object}; events - [an array]
        profile = {}
        profile["gamer"] = gamer.data
        profile["events"] = events.data

        return Response(profile)
    

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for gamer's related Django user"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class GamerSerializer(serializers.ModelSerializer):
    """JSON serializer for gamers"""
    user = UserSerializer(many=False)

    class Meta:
        model = Gamer
        fields = ('user', 'bio')


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    class Meta:
        model = Game
        fields = ('name',)


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""
    game = GameSerializer(many=False)

    class Meta:
        model = Event
        fields = ('id', 'game', 'name', 'time')
        
        
# 附 expected response:    
{
  "gamer": {
    "user": {
      "first_name": "Emily",
      "last_name": "Lemmon",
      "username": "me@me.com"
    },
    "bio": "Outgoing and funny. Always have the best interests of other at heart."
  },
  "events": [
    {
      "id": 3,
      "url": "http://localhost:8000/events/3",
      "game": {
        "title": "Dungeons & Dragons"
      },
      "description": "Vale of the Frost King campaign. All weekend.",
      "date": "2021-04-20",
      "time": "08:00:00"
    },
    {
      "id": 10,
      "url": "http://localhost:8000/events/10",
      "game": {
        "title": "Welcome To"
      },
      "description": "Lightning round welcome to session. Cards will be turned every minute. Drinking involved.",
      "date": "2020-11-11",
      "time": "17:30:00"
    }
  ]
}