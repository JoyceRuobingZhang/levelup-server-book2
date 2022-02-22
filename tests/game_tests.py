import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import Gametype, Game, Gamer


class GameTests(APITestCase):
    # If you need to have any resources created ❗️before a test is run, you can do that in setUp()
    def setUp(self):
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }
        # Initiate request and capture response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Store the auth token
        self.token = json_response["token"]

        # Assert that a user was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # SEED DATABASE WITH ONE GAME TYPE
        # This is needed because the API does not expose a /gametypes
        # endpoint for creating game types
        gametype = Gametype()
        gametype.label = "Board game"
        gametype.save()


    def test_create_game(self):
        """
        Ensure we can create a new game.
        """
        # DEFINE GAME PROPERTIES
        url = "/games"
        data = {
            "gametype_id": 1,
            "name": "Clue",
            # "created_by": "Milton Bradley",
            "player_limit": 6,
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["name"], "Clue")
        # self.assertEqual(json_response["createdBy"], "Milton Bradley")
        self.assertEqual(json_response["playerLimit"], 6)
        # self.assertEqual(json_response["skill_level"], 5)
        
        
    def test_get_game(self):
        """
        Ensure we can get an existing game.
        """

        # Seed the database with a game
        game = Game()
        game.gametype_id = 1
        game.name = "Monopoly"
        game.player_limit = 4
        # game.skill_level = 5
        # game.maker = "Milton Bradley"
        
        gamer = Gamer.objects.get(pk=1)
        game.created_by = gamer

        game.save()

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/games/{game.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["name"], "Monopoly")
        self.assertEqual(json_response["playerLimit"], 4)
        # self.assertEqual(json_response["maker"], "Milton Bradley")
        # self.assertEqual(json_response["skill_level"], 5)



    def test_change_game(self):
        """
        Ensure we can change an existing game.
        """
        game = Game()
        game.gametype_id = 1
        game.name = "Sorry"
        # game.skill_level = 5
        # game.maker = "Milton Bradley"
        game.player_limit = 4
        game.gamer_id = 1
        
        gamer = Gamer.objects.get(pk=1)
        game.created_by = gamer
        
        game.save()

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "gametypeId": 1,
            # "skillLevel": 2,
            "name": "Sorry",
            # "maker": "Hasbro",
            "playerLimit": 4
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/games/{game.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY CHANGES
        response = self.client.get(f"/games/{game.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties are correct
        self.assertEqual(json_response["name"], "Sorry")
        # self.assertEqual(json_response["maker"], "Hasbro")
        # self.assertEqual(json_response["skill_level"], 2)
        self.assertEqual(json_response["playerLimit"], 4)
        
        
    def test_delete_game(self):
        """
        Ensure we can delete an existing game.
        """
        game = Game()
        game.gametype_id = 1
        game.name = "Sorry"
        # game.skill_level = 5
        # game.maker = "Milton Bradley"
        game.player_limit = 4
        # game.gamer_id = 1
        
        gamer = Gamer.objects.get(pk=1)
        game.created_by = gamer
        
        game.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY 404 response
        response = self.client.get(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)