"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response # 📌 Response will attach the headers, status to the JSON data.
from rest_framework import serializers # 📌 serializers will serialize the data (make it a dictionary), and make it JSON format.
from rest_framework import status
from levelupapi.models import Game, Gametype, Gamer
from django.db.models import Count

class GameView(ViewSet):
    """Level up games"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """

        # Uses the token passed in the `Authorization` header
        gamer = Gamer.objects.get(user=request.auth.user)

        game = Game() #❗️Create a new Python instance of the Game class
        game.name = request.data["name"] # and set its properties from what was sent in the body of the request from the client.
        game.player_limit = request.data["player_limit"]
        # game.skill_level = request.data["skillLevel"]
        game.created_by = gamer

        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the `gameTypeId` in the body of the request.
        gametype = Gametype.objects.get(pk=request.data["gametype_id"])
        game.gametype = gametype

        # Try to save the new game to the database, then serialize the game instance as JSON, 
        # and send the JSON as a response to the client request
        try:
            game.save()
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as ex:
            return HttpResponseServerError(ex)
        

    def update(self, request, pk=None): 
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        # import pdb; pdb.set_trace()
        game_type = Gametype.objects.get(pk=request.data["gametype_id"])
        

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        game = Game.objects.get(pk=pk)
        game.name = request.data["name"]
        game.player_limit = request.data["player_limit"]
        game.created_by = gamer 
        game.gametype = game_type
        # game.gamer = gamer
        # game.maker = request.data["maker"]
        # game.skill_level = request.data["skillLevel"]

        game.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    

    def destroy(self, request, pk=None): # or def destroy(self, *args, **kwargs):
        # kwargs stands for keyword arguments
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            game = Game.objects.get(pk=pk) # pk = kwargs.pop(‘pk’)
            game.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def list(self, request):
        """ Handle GET requests to games resource
        Returns:
            Response -- JSON serialized list of games  """
        # Get all game records from the database
        games = Game.objects.all()
        # count how many events are there for each game
        games = Game.objects.annotate(event_count=Count('events'))
        
        # Support filtering games by type： http://localhost:8000/games?type=1
        # That URL will retrieve all tabletop games
        game_type = self.request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(gametype__id=game_type)
            # gametype__id has to be a double-underscore.
            # The use of the dunderscore (__) here represents a join operation (foreign-key table).
            # for it's own table, do one underscore

        serializer = GameSerializer(
            games, many=True, context={'request': request})
        
        # serializer.data.append(gamer)
        return Response(serializer.data)
    
    
class GameSerializer(serializers.ModelSerializer):
    """ JSON serializer for games
    Arguments:
        serializer type  """
    class Meta:
        model = Game
        fields = ('id', 'name', 'player_limit', 'created_by', 'gametype', 'event_count') #the properties in the model
        depth = 2  # relationship depth  <10
        
