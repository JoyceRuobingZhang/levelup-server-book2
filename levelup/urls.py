from django.conf.urls import include
from django.urls import path
from levelupapi.views import register_user, login_user
from rest_framework import routers
from levelupapi.views import GameTypeView, GameView, EventView, ProfileView  # import view classes

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'gameTypes', GameTypeView, 'gametype')  # part of the controller.  "r" means regex
router.register(r'games', GameView, 'game')  
router.register(r'events', EventView, 'event')
router.register(r'profile', ProfileView, 'profile')


# controller-code
urlpatterns = [
    path('', include(router.urls)),
    
    # Requests to http://localhost:8000/register will be routed to the register_user function
    path('register', register_user),
    
    # Requests to http://localhost:8000/login will be routed to the login_user function
    path('login', login_user),
    
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]

