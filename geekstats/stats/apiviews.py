
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.db.models import F, Count, Sum, Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.parsers import JSONParser

from .geekmodels import Maps, MapRating, Geek, TiersData, Season, Team, TeamGeek
from .serializers import MapSerializer, MapImageSerializer, DataSerializer, MapRequestSerializer, TeamSetSerializer, StatRequestSerializer, BotMapSerializer
from datetime import date, timedelta
from decimal import Decimal
from django.utils import timezone


import os, json

@api_view(['GET','POST'])
# @renderer_classes((TemplateHTMLRenderer, JSONRenderer))

def map_rating(request):
    if request.method == 'GET':
        return HttpResponse("Not Implemented")
    elif request.method == 'POST':
        serializer = MapSerializer(data=request.data)
        if serializer.is_valid():
            try:
                map_id = Maps.objects.get(idmap=serializer.data['map_id'])
                user_id = Geek.objects.get(geek_id=serializer.data['user_id'])
            except:
                return Response('Map or Geek is invalid', status=status.HTTP_400_BAD_REQUEST)                
            map_rating = serializer.data['rating']
            try:
                check_rating = MapRating.objects.get(map_id=map_id, geek_id=user_id)
                check_rating.rating = map_rating
                check_rating.save()
                return Response("Map has been updated", status=status.HTTP_201_CREATED)
            except:
                MapRating.objects.create(map=map_id, geek=user_id, rating=map_rating)
                return Response("Map created", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','POST'])
# @renderer_classes((TemplateHTMLRenderer, JSONRenderer))

def bot_map_rating(request):
    if request.method == 'GET':
        return HttpResponse("Not Implemented")
    elif request.method == 'POST':
        serializer = BotMapSerializer(data=request.data)
        if serializer.is_valid():
            map_rating = serializer.data['rating']
            print(serializer.data['map'], serializer.data['user'], map_rating)
            if map_rating == -1:                                                                # TO LOOKUP MAPS BY PARTIAL NAME
                map_id = Maps.objects.filter(map__contains=serializer.data['map']).order_by('last_play')[:5]
                print(map_id.values('map','idmap'))
                return Response(map_id.values('idmap','map','thumbnail','description',), status=status.HTTP_200_OK)
            elif map_rating == -2:                                                    # TO SEE THIS WEEK's MAPS
                map_id = Maps.objects.order_by('last_play')[:3]
                return Response(map_id.values('idmap','map','thumbnail','description',), status=status.HTTP_200_OK)
            elif map_rating == -3:                                                    # TO SEE THE MAP VOTES
                map_id = Maps.objects.filter(map__contains=serializer.data['map']).order_by('map')[:1]
                map_rating = MapRating.objects.annotate(map_name=F('map_id__map')).values('map_name').filter(map_id=map_id).annotate(
                    vote_count= Count('geek_id'),
                    vote_sum = Sum('rating')
                    )
                print(map_rating)
                return Response(map_rating.values('map_name', 'vote_count', 'vote_sum'), status=status.HTTP_200_OK)
            elif map_rating > 0 and map_rating < 6:                                                    # PROCESS THE VOTE
                map_id = Maps.objects.filter(map=serializer.data['map']).first()
                if map_id is None:
                    return Response('Map does not exist', status=status.HTTP_400_BAD_REQUEST)
                user_id = Geek.objects.filter(discord=serializer.data['user']).first()
                print(user_id)
                if user_id is None:
                    return Response('Geek does not exist', status=status.HTTP_400_BAD_REQUEST)
                api_key = os.getenv("VOTE_API_KEY")
                if serializer.data['key'] == api_key:
                    try:
                        check_rating = MapRating.objects.get(map_id=map_id, geek_id=user_id)
                        check_rating.rating = map_rating
                        check_rating.save()
                        return Response("Map has been updated", status=status.HTTP_201_CREATED)
                    except:
                        MapRating.objects.create(map=map_id, geek=user_id, rating=map_rating)
                        return Response("Map created", status=status.HTTP_201_CREATED)
                else:
                    return Response('You are not authorized to update this data', status=status.HTTP_400_BAD_REQUEST)
                
            else:
                return Response('Invalid rating', status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
@api_view(['GET','POST'])
def upload_image(request):
    if request.method == 'GET':
        return HttpResponse("Not Implemented")
    elif request.method == 'POST':
        serializer = MapImageSerializer(data=request.data)
        if serializer.is_valid():
            mid = serializer.data['mid']
            print('map is:'+str(mid))
            print('field is:'+serializer.data['type'])
            # mid = request.POST.get('mid')
            map_update = Maps.objects.get(idmap=mid)
            if  serializer.data['type'] == 'hero':
                map_update.hero_image  =  request.FILES.get('image')
            elif serializer.data['type'] == 'radar':
                map_update.radar  =  request.FILES.get('image')
            elif serializer.data['type'] == 'image2':
                map_update.image2  =  request.FILES.get('image')
            elif serializer.data['type'] == 'thumb':
                map_update.thumbnail  =  request.FILES.get('image')
            else:
                map_update.image3  =  request.FILES.get('image')

            # map_update.image2 = request.FILES.get('image2') if request.FILES.get('image2') else map_update.image2
            # map_update.thumbnail = request.FILES.get('thumb') if request.FILES.get('thumb') else map_update.thumbnail
            # print(dataMap[0])
            try:
                map_update.save()
            except:
                print('save failed:'+str(request.FILES.get('image')))
            return Response("map image has been updated", status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def update_data(request):
    if request.method == 'GET':
        return HttpResponse("Not Implemented")
    elif request.method == 'POST':
        serializer = DataSerializer(data=request.data)
        if serializer.is_valid():
            field = serializer.data['field']
            value = serializer.data['value']
            curr_user = serializer.data['uid']
            if field =='theme' or  field =='description' or field =='workshop_link':
                edit_map = Maps.objects.get(idmap=serializer.data['did'])
                setattr(edit_map, field, value)
                # edit_map[field] = value
                try:
                    edit_map.save()
                    return Response("Map updated", status=status.HTTP_200_OK)
                except:
                    print('update failed: '+serializer.data[field]+' = '+serializer.data[value])
                    return Response("invalid update", status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def get_image(request):
    if request.method == 'POST':
        return HttpResponse("Not Implemented")
    elif request.method == 'GET':
        print("data",request.query_params)
        serializer = MapRequestSerializer(data=request.query_params)
        if serializer.is_valid():
            mid = serializer.data['mid']
            map_name = serializer.data['map']
            if serializer.data['type'] == 'thumb':
                print('map is:'+map_name)
                print('field is:'+serializer.data['type'])
                map_image = Maps.objects.get(map=map_name)
                if map_image.thumbnail:
                    return Response(map_image.thumbnail.url, status=status.HTTP_200_OK)
                else :
                    return Response("No Map Image", status=status.HTTP_200_OK)
            else :
                return Response("Not Implemented", status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, date):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


@api_view(['GET','POST'])
def get_player_stats(request):
    if request.method == 'POST':
        return HttpResponse("Not Implemented")
    elif request.method == 'GET':
        serializer = StatRequestSerializer(data=request.query_params)
        if serializer.is_valid():
            player = serializer.data['player']
            start_date = serializer.data['start_date']
            end_date = serializer.data['end_date']
            if player == 'none':
                from django.db.models import Avg, Sum, Min
                player_stats = TiersData.objects.filter(matchdate__gte=start_date, matchdate__lte=end_date).values('player').annotate(
                    tier=Min('tier'),
                    alltime_kdr=Min('alltime_kdr'),
                    last90_kdr=Min('last90_kdr'),
                    year_kdr=Min('year_kdr'),
                    kills=Sum('kills'),
                    deaths=Sum('deaths'),
                    assists=Sum('assists'),
                    kdr=Avg('kdr'),
                    akdr=Avg('akdr'),
                    adr=Avg('ADR')
                )
                print(player_stats.query)
            else:
                player_stats = TiersData.objects.values('player','tier','matchdate','kills','deaths','assists','kdr','alltime_kdr','adr').filter(player=player,matchdate__gte=start_date,matchdate__lte=end_date)
            player_stats_d = list(player_stats)
            j_stats = json.dumps(player_stats_d, cls=CustomEncoder)
            return JsonResponse(j_stats, safe=False)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# write and API that will take two captains and a season name and write the captains into the season table

@api_view(['GET','POST'])


def pick_teams(request):
    if request.method == 'POST':
        # data = JSONParser().parse(request)
        print(request.data)
        serializer = StatRequestSerializer(data=request.data)
    elif request.method == 'GET':
        serializer = StatRequestSerializer(data=request.query_params)
    else:
        return HttpResponse("Not Implemented")
    if serializer.is_valid():
        # print(serializer.data['players'][0])
        captain1 = serializer.data['cap1']
        captain2 = serializer.data['cap2']
        today_plus_seven = timezone.now().date() + timedelta(days=7)
        seasons = Season.objects.filter(start_date__lte=today_plus_seven, end_date__gte=today_plus_seven)
        captains = {}
        if seasons.exists() and seasons.count() == 1:
            if captain1 != 'none' and captain2 != 'none':
                cap1 = Geek.objects.filter(Q(handle__iexact=captain1) | Q(discord__iexact=captain1), is_member=1)
                print('cap1', captain1, cap1)
                cap2 = Geek.objects.filter(Q(handle__iexact=captain2) | Q(discord__iexact=captain2), is_member=1)
                print('cap2', captain2, cap2)
                if cap1.exists() and cap2.exists():
                    cap1 = cap1.first()
                    cap2 = cap2.first()
                    captains = {
                        'captain1_csgo': cap1.csgo_id,
                        'captain1': cap1.handle,
                        'captain2_csgo': cap2.csgo_id, 
                        'captain2': cap2.handle,
                        'status': 'Captains updated',
            }        

                else:
                    print('One or both of the captains do not exist')
                    return Response("One or both of the captains do not exist", status=status.HTTP_400_BAD_REQUEST)
                for season in seasons:
                    teams = Team.objects.filter(season=season)
                    if teams.count() == 2:
                        team1, team2 = teams
                        team1.captain = cap1
                        team1.save()
                        team2.captain = cap2
                        team2.save()
                    else:
                        return Response("The teams have not been created for this season", status=status.HTTP_400_BAD_REQUEST)
            players = serializer.data['players']
            print('players:', players, type(players))
            if players == []:
                return Response("No players have been submitted", status=status.HTTP_400_BAD_REQUEST)
            # player_list = Geek.objects.filter(discord__in=players)
            player_list = Geek.objects.filter(discord__in=players).annotate(steam_id=F('csgo_id'))
            print(player_list.query, player_list)
        # Create a dictionary with the csgo_id of the captains
            data = {
                'captains': captains,
                'players': list(player_list.values('steam_id', 'discord', 'handle')),
                'season': seasons.first().name
            }        
            # Convert the dictionary to a JSON string
            # captains_json = json.dumps(captains)
            
            # Return the JSON string
            print(data)
            return JsonResponse(data, safe=False)
            # return Response("Captains updated", status=status.HTTP_200_OK)
        else:
            return Response("There is no season created in the range of today's date.", status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','POST'])
def save_teams(request):
    # test_data = {'team_a': {'players': [{'player_name': 'Cloner', 'player_score': 2.2507}, {'player_name': 'Duckhead', 'player_score': 0.8698}, {'player_name': 'Toze', 'player_score': 1.1778}, {'player_name': 'Yakobay', 'player_score': 0.9579}, {'player_name': 'Ogre', 'player_score': 0.6471}], 'team_name': 'Alpha', 'team_num_players': 5, 'team_score': 5.9032627425, 'captain': 'Yakobay'}, 'team_b': {'players': [{'player_name': 'Dream', 'player_score': 1.9214}, {'player_name': 'Edge', 'player_score': 1.2822}, {'player_name': 'Mailboxhead', 'player_score': 1.0127}, {'player_name': 'Unthink', 'player_score': 1.5904}], 'team_name': 'Bravo', 'team_num_players': 4, 'team_score': 5.8066908706, 'captain': 'Mailboxhead'}}
    if request.method == 'POST':
        print(request.data)
        # data = JSONParser().parse(request)
        serializer = TeamSetSerializer(data=request.data)
    else:
        return HttpResponse("Not Implemented")
    if serializer.is_valid():
        today_plus_seven = timezone.now().date() + timedelta(days=7)
        season = Season.objects.filter(start_date__lte=today_plus_seven, end_date__gte=today_plus_seven).first()
        if season is None:
            return Response("There is no season created in the range of today's date.", status=status.HTTP_404_NOT_FOUND)
# INITIALIZE POST DATA
        captain1 = serializer.validated_data['cap1']
        captain2 = serializer.validated_data['cap2']
        team1 = serializer.validated_data['team1']
        team2 = serializer.validated_data['team2']
        players1 = serializer.validated_data['players1']
        players2 = serializer.validated_data['players2']
        players1_list = players1[0].strip('[]').replace('"', '').split(', ')
        players2_list = players2[0].strip('[]').replace('"', '').split(', ')
        
        print(players1_list, players2_list)
        print(players1_list[1])

# GET THE TEAMS FOR THE CURRENT SEASON
        teams = Team.objects.filter(season=season)
        team_a = teams.first()
        team_b = teams.last()
        print('DATA:',  captain1, captain2, team1, team2, players1, players2)

# CHECK THAT THE CAPTAINS ARE VALID AND THAT THEY ARE THE CAPTAINS FOR THE CURRENT SEASON
        cap1 = Geek.objects.values('discord','handle').filter(Q(handle=captain1) | Q(discord=captain1), is_member=1)
        cap2 = Geek.objects.values('discord','handle').filter(Q(handle=captain2) | Q(discord=captain2), is_member=1)
        # print('CAPTAINS:', cap1, cap2)
        # print('TEAMS:', teams, team1, team2)
        
        if cap1.exists() and cap2.exists() and cap1[0]['handle'] == captain1 and cap2[0]['handle'] == captain2:
            for geek in players1_list:
                player = Geek.objects.filter(Q(handle=geek) | Q(discord=geek), is_member=1)
                if player.exists():
                    teamGeekCheck = TeamGeek.objects.filter(team=teams.first(), geek_id=player.first().geek_id)
                    if teamGeekCheck.exists():
                        print(geek + " already exists in the team: "+ team_a.name)
                        continue
                    else:
                        teamGeek = TeamGeek.objects.create(team=team_a, geek_id=player.first().geek_id, tier_id = player.first().tier_id)
                        teamGeek.save()
                else:
                    return Response(geek + " does not exist in our database", status=status.HTTP_400_BAD_REQUEST)
            for geek in players2_list:
                player = Geek.objects.filter(Q(handle=geek) | Q(discord=geek), is_member=1)
                if player.exists():
                    teamGeekCheck = TeamGeek.objects.filter(team=team_b, geek_id=player.first().geek_id)
                    if teamGeekCheck.exists():
                        print(geek + " already exists in the team: "+ team_b.name)
                        continue
                    else:
                        teamGeek = TeamGeek.objects.create(team=teams.last(), geek_id=player.first().geek_id, tier_id = player.first().tier_id)
                        teamGeek.save()
                else:
                    return Response(geek + " does not exist in our database", status=status.HTTP_400_BAD_REQUEST)
            return Response("Team has been created", status=status.HTTP_200_OK)

        else:
            return Response("One or both of the captains do not exist or these are not the right team captains for the current season teams", status=status.HTTP_400_BAD_REQUEST)
    else:
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





