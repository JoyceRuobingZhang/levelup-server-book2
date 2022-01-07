"""View module for handling requests about game types"""
# The ViewSet will only handle GET requests sent from a client application over the HTTP protocol. 
# You don't want to support POST, PUT, or DELETE 
# because you don't want clients to have the ability to create, edit, or remove game types from the database.

from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from levelupapi.models import Gametype


# part of the controller
# in Django, part of the controller-level-code is called ViewSet
#  M V C  is just a concept

class GameTypeView(ViewSet):
    """Level up game types"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            game_type = Gametype.objects.get(pk=pk)  # model-layer
            serializer = GameTypeSerializer(game_type, context={'request': request}) # view-layer
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        gametypes = Gametype.objects.all()

        # Note the additional `many=True` argument to the serializer. 
        # It's needed when you are serializing a list of objects instead of a single object.
        serializer = GameTypeSerializer(
            gametypes, many=True, context={'request': request})
        return Response(serializer.data)
    
    
class GameTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for game types 
    
    Arguments: serializers"""
    
    class Meta:
        model = Gametype
        fields = ('id', 'label')