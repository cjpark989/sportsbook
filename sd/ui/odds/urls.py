from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # Game description
    path("game/<str:game_description>/", views.game, name="game"),
]
