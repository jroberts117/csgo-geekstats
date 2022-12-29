from django.urls import path
import sys

from . import views, apiviews

urlpatterns = [
    path('', views.tiers, name='index'),
    path('Geeks', views.geeks, name='geeks'),
    path('Awards', views.awards, name='awards'),
    path('Teams', views.teams, name='teams'),
    path('Weapons', views.weapons, name='weapons'),
    path('Tiers', views.tiers, name='tiers'),
    path('Maps', views.maps, name='maps'),
    path('Map2', views.map2, name='map2'),
    path('About', views.about, name='about'),
    path('PlayerDetails', views.playerdetails, name='playerdetails'),
    path('Details', views.details, name='details'),
    # path('Event', views.gfxx, name='gfxx'),
    path('Buys', views.buys, name='buys'),
    path('GFMMXXII', views.event, name='event'),
    path('rating/', apiviews.map_rating, name='map_rating'),
    path('mapimg/', apiviews.upload_image, name='upload_image'),
]
