from django.urls import path
from .views.registration import UserRegistration
from .views.authorization import UserAuthorization
from .views.session import UserSession
urlpatterns = [
    path('reg/', UserRegistration.as_view(), name='registration'),
    path('login/',  UserAuthorization.as_view(), name='authorization'),
    path('status/', UserSession.as_view(), name='status'),
        ]
