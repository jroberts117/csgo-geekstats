from django.urls import path
import sys

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Geeks', views.geeks, name='geeks'),
    path('Awards', views.awards, name='awards'),
    path('Teams', views.teams, name='teams'),
    path('Weapons', views.weapons, name='weapons'),
    path('Tiers', views.tiers, name='teams'),
    path('Maps', views.maps, name='maps'),
    path('About', views.about, name='about'),
    path('PlayerDetails', views.playerdetails, name='playerdetails'),
    path('Details', views.details, name='details'),
    path('Event', views.gfxx, name='gfxx'),
    path('Buys', views.buys, name='buys'),
]
