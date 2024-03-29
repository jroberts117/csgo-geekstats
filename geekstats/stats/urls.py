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
    path('MapDetails', views.mapdetails, name='map detail'),
    path('Map2', views.map2, name='map2'),
    path('About', views.about, name='about'),
    path('api', views.api, name='api'),
    path('PlayerDetails', views.playerdetails, name='playerdetails'),
    path('Details', views.details, name='details'),
    # path('Event', views.gfxx, name='gfxx'),
    path('Buys', views.buys, name='buys'),
    #path('GFMMXXII', views.event, name='event'),
    path('GFMMXXIII', views.event, name='event'),
    path('rating/', apiviews.map_rating, name='map_rating'),
    path('botrating/', apiviews.bot_map_rating, name='bot_map_rating'),
    path('mapimg/', apiviews.upload_image, name='upload_image'),
    path('getimg/', apiviews.get_image, name='get_image'),
    path('dataupdate/', apiviews.update_data, name='update_data'),
    path('playerstats/', apiviews.get_player_stats, name='get_player_stats'),
    path('pick_teams/', apiviews.pick_teams, name='pick_teams'),
    path('save_teams/', apiviews.save_teams, name='save_teams'),
    # path('ai/', apiviews.ai_request, name='ai_request'),

]
