from django.forms import DecimalField, IntegerField
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse
from django.template import loader
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from .geekmodels import Buy, Geek, GeekKDRHistory, TeamWins, TiersData, Frag, MatchRound, Death, SeasonMatch, GeekInfo, FragDetails, GeekfestMatchAward, AwardCategory, Season, GeekAuthUser, MapData, SeasonWins, TeamGeek, Tier, Team, Maps, MapRating, Damage
from .geekclasses import season, player, map_summary
import stats.functions as func
from .forms import CustomUserCreationForm, GeeksForm
import logging
import operator, sys
from django.db import models
from django.db.models import Count, Sum, Avg, Min, Max, Q, F, ExpressionWrapper, Value
import datetime
import uuid
import pygal
from pygal.style import Style
from datetime import date, timedelta
from collections import defaultdict, Counter
from itertools import groupby

###############################################################
## Views
## This is the page dispatch based on the URL being called for the site
## The goal here was to keep the processing to a minimum and keep
## the dispatch to the site simple.
## This code block links the functions to the templates rendered for the browser
###############################################################

#################  Class Definitions ##########################
#--------------------------------------------------------------#
#-- Class:  StateInfo
#--         used to set the active page for the menu and title
#--------------------------------------------------------------#

class StateInfo:
    def __init__(self):
        self.menu = ['Awards','Tiers','Seasons','Weapons','Maps','Map Details','Geeks']
        self.page = ['Awards','Tiers','Teams','Weapons','Maps','MapDetails','Geeks']
##        self.menu = ['Tiers','Teams','Maps','Weapons','Geeks']
        self.state = ['','','','','','','', '', '']

    def set(self, value):
        for idx, val in enumerate(self.menu):
            if val == value:
                self.state[idx] = 'active'
            else:
                self.state[idx] = ''
#--------------------------------------------------------------#
#-- Class:  state
#--         used to track key state data like the current dates
#--         being used, or the data needed for a query
#--------------------------------------------------------------#

class state:
    def __init__(self):
        self.start_date = '2019-02-09'
        self.end_date = '2019-02-09'
        self.today = date.today().isoformat()
        self.days90ago = date.today() - timedelta(days=90)
        self.days180ago = date.today() - timedelta(days=180)
        self.compare = ''
        self.value = 0
        self.clause = ''
        self.page = ''
        self.season = ''
        self.selector = ''
        self.event_dates = func.unique_dates(list(SeasonMatch.objects.values('match_date').distinct().filter(~Q(map='None')).order_by('-match_date')))
        self.seasons = list(Season.objects.values('name').distinct().order_by('-start_date'))
        self.datetype = ''
    def setsession(self,start,end,compare,value,page, selector, datetype):
        self.start_date = start
        self.end_date = end
        self.compare = compare
        self.value = value
        self.page = page
        self.selector = selector
        self.datetype = datetype
        self.event_dates = func.unique_dates(list(SeasonMatch.objects.values('match_date').distinct().filter(~Q(map='None')).order_by('-match_date')))
        self.seasons = list(Season.objects.values('name').distinct().order_by('-start_date'))

#################  Global Variables ##########################
mainmenu = StateInfo()
newstate = state()
#################  Functions ##########################
def listbuilder(lst,type):
    xlst = []
    for i in lst:
        xlst.append(i[type])
    wlst = Counter(xlst)
    nlist = []
    for x in wlst:
        nlist.append({type:x,'id__count':wlst[x]})
    nlist = sorted(nlist, key=lambda d: d['id__count'], reverse=True)
    return(nlist)

def index(request):
##    geeks = Geeks.objects.order_by('handle')
    template = loader.get_template('index.html')
    context = {'title': 'GeekFest Stats'}
    return HttpResponse(template.render(context, request))

#    █████████   █████   ███   █████   █████████   ███████████   ██████████    █████████ 
#   ███░░░░░███ ░░███   ░███  ░░███   ███░░░░░███ ░░███░░░░░███ ░░███░░░░███  ███░░░░░███
#  ░███    ░███  ░███   ░███   ░███  ░███    ░███  ░███    ░███  ░███   ░░███░███    ░░░ 
#  ░███████████  ░███   ░███   ░███  ░███████████  ░██████████   ░███    ░███░░█████████ 
#  ░███░░░░░███  ░░███  █████  ███   ░███░░░░░███  ░███░░░░░███  ░███    ░███ ░░░░░░░░███
#  ░███    ░███   ░░░█████░█████░    ░███    ░███  ░███    ░███  ░███    ███  ███    ░███
#  █████   █████    ░░███ ░░███      █████   █████ █████   █████ ██████████  ░░█████████ 
# ░░░░░   ░░░░░      ░░░   ░░░      ░░░░░   ░░░░░ ░░░░░   ░░░░░ ░░░░░░░░░░    ░░░░░░░░░  
                                                                                       
                                                                                       
def awards(request):
    mainmenu.set('Awards')
    template = loader.get_template('awards.html')
    newstate.setsession(request.session['start_date'],request.session['end_date'],'',0,'Awards', request.session['selector'],request.session['datetype'])
    try:
        newstate.value=request.GET['aid']
        request.session['aid'] = newstate.value
    except:
        try:
            newstate.value = request.session['aid']
        except:
            newstate.value = 0

    endDate = datetime.datetime.strptime(request.session['end_date'], '%Y-%m-%d') + datetime.timedelta(days=1)
    raw_award_data = GeekfestMatchAward.objects.select_related('match', 'geefest_award', 'geekfest_award__award_category', 'geek').filter(
        match__match_date__gte=request.session['start_date'], match__match_date__lte=endDate.strftime('%Y-%m-%d %H:%M:%S')).values(
            'geek__handle', 'geekfest_award__award_name', 'geekfest_award__award_title', 'geekfest_award__award_category__category_name',
            'geekfest_award__award_image_path', 'geekfest_award__award_description', 'geekfest_award__award_value_type',
            'geekfest_award__award_category__category_color','geekfest_award__award_category__award_category_id').annotate(
                max_points=Max('award_value'), sum_points=Sum('award_value'), min_points=Min('award_value')).order_by(
                    "geekfest_award__award_category__award_category_id", "geekfest_award__award_name")

    award_data_by_award = defaultdict(list)
    for award_data in raw_award_data:
        award_data_by_award[award_data['geekfest_award__award_name']].append(award_data)


    awards_new = []

    for award_name in award_data_by_award:
        if (award_data_by_award[award_name] is None and len(award_data_by_award[award_name]) > 0):
            continue
        sample = award_data_by_award[award_name][0]
        award_value_type = sample['geekfest_award__award_value_type']
        data_key = 'sum_points'
        reverse = True
        if award_value_type == 'max':
            data_key = 'max_points'
        elif award_value_type == 'min':
            data_key = 'min_points'
            reverse = False
        #print(award_data_by_award[award_name])
        ad = award_data_by_award[award_name]
        ad.sort(key=lambda aw: aw[data_key], reverse=reverse)
        winner_award_data = []
        for aw in ad[:5]:
            aw_value = aw[data_key]
            if aw_value == aw_value.to_integral_value():
                aw_value = int(aw_value)
            winner_award_data.append([aw['geek__handle'], aw_value])
        #winner_award_data = map(lambda ad: {ad['geek__handle'], ad['sum_points']}, ad[:5])
        actual_award = func.awards(sample['geekfest_award__award_title'], winner_award_data, award_name, sample['geekfest_award__award_category__category_name'],
            sample['geekfest_award__award_image_path'], sample['geekfest_award__award_description'], sample['geekfest_award__award_category__category_color'],
            sample['geekfest_award__award_category__award_category_id'])
        # print(actual_award)
        awards_new.append(actual_award)

    def award_type_key_func(aw):
        return aw.groupid

    awards_new = sorted(awards_new, key=award_type_key_func)

    awards_by_type = {}
    for key, awards in groupby(awards_new, award_type_key_func):
        awards_by_type[key] = list(awards)

    award_types = []
    for category in AwardCategory.objects.all():
        award_types.append([category.category_name, category.category_color, category.award_category_id, (awards_by_type.get(category.award_category_id) or [])])

            
    #award_types, awards = func.get_awards(newstate)
    context = {'awards': awards_new,
               'abt': awards_by_type, 
               'types' : award_types,
               'title': 'GeekFest Awards',
               'stateinfo': zip(mainmenu.menu,mainmenu.state),
               'state':newstate,
               }
    return HttpResponse(template.render(context, request))

#  ███████████ ██████████   █████████   ██████   ██████  █████████ 
# ░█░░░███░░░█░░███░░░░░█  ███░░░░░███ ░░██████ ██████  ███░░░░░███
# ░   ░███  ░  ░███  █ ░  ░███    ░███  ░███░█████░███ ░███    ░░░ 
#     ░███     ░██████    ░███████████  ░███░░███ ░███ ░░█████████ 
#     ░███     ░███░░█    ░███░░░░░███  ░███ ░░░  ░███  ░░░░░░░░███
#     ░███     ░███ ░   █ ░███    ░███  ░███      ░███  ███    ░███
#     █████    ██████████ █████   █████ █████     █████░░█████████ 
#    ░░░░░    ░░░░░░░░░░ ░░░░░   ░░░░░ ░░░░░     ░░░░░  ░░░░░░░░░  
                                                                 
                                                                 
                                                                 
def teams(request):
    ### INITIALIZE THE PAGE
    mainmenu.set('Teams')
    template = loader.get_template('teams.html')

    if request.session['datetype'] != 'season':
        curr_season = Season.objects.values().order_by('-start_date')
        request.session['season'] = curr_season[0]['name']
        request.session['start_date'] = curr_season[0]['start_date'].strftime('%Y-%m-%d')
        request.session['end_date'] = curr_season[0]['end_date'].strftime('%Y-%m-%d')
        request.session['datetype'] = 'season'

    newstate.setsession(request.session['start_date'],request.session['end_date'],'',0,'Teams', request.session['selector'],request.session['datetype'])

    try:
        newstate.season = request.session['season']
    except:
        request.session['season'] = 'Rock The Vote'
        newstate.season = request.session['season']

    tab = 0
    # except:
    #     newstate.season = 'Unspecified'

    ### PROCESS ANY FORMS SUBMITTED
    if request.POST.get('team1mbrs'):
        team1 = request.POST.get('team1')
        team2 = request.POST.get('team2')
        tab = 1
        team1mbrs = request.POST.getlist('team1mbrs')
        team2mbrs = request.POST.getlist('team2mbrs')
        # print(team2mbrs)
        team1capt = int(request.POST.get('team1capt'))
        team2capt = int(request.POST.get('team2capt'))
        team1cocapt = int(request.POST.get('team1cocapt'))
        team2cocapt = int(request.POST.get('team2cocapt'))
        # print('co-cap',str(team2cocapt))
        curr_team1 = TeamGeek.objects.filter(team__name=team1)
        curr_team1.delete()
        for i in team1mbrs:
            id = Geek.objects.get(geek_id=int(i))
            team = Team.objects.get(name=team1)
            tier = Tier.objects.get(tier_name=id.tier)
            currTEST_team1 = TeamGeek(geek=id, team=team, tier=tier)
            currTEST_team1.save()
        team.captain_id = team1capt
        team.co_captain_id = team1cocapt
        team.save()
        curr_team2 = TeamGeek.objects.filter(team__name=team2)
        curr_team2.delete()
        for i in team2mbrs:
            id = Geek.objects.get(geek_id=int(i))
            team = Team.objects.get(name=team2)
            tier = Tier.objects.get(tier_name=id.tier)
            currTEST_team2 = TeamGeek(geek=id, team=team, tier=tier)
            currTEST_team2.save()
        team.captain_id = team2capt
        team.co_captain_id = team2cocapt
        team.save()
    elif request.POST.get('seasonName'):
        name = request.POST.get('seasonName')
        start = request.POST.get('startDate')
        end = request.POST.get('endDate')
        team1 =  request.POST.get('team1Name')
        team1desc =  request.POST.get('team1Desc')
        team2 =  request.POST.get('team2Name')
        team2desc =  request.POST.get('team2Desc')
        team1capt = int(request.POST.get('team1capt'))
        team2capt = int(request.POST.get('team2capt'))
        team1cocapt = int(request.POST.get('team1cocapt'))
        team2cocapt = int(request.POST.get('team2cocapt'))
        curr_temp_season = Season(name=name, start_date=start, end_date=end)
        curr_temp_season.save()
        curr_temp_team1 = Team(season_id=curr_temp_season.season_id, name=team1, description=team1desc, captain_id=team1capt, co_captain_id=team1cocapt)
        curr_temp_team1.save()
        curr_temp_team2 = Team(season_id=curr_temp_season.season_id, name=team2, description=team2desc, captain_id=team2capt, co_captain_id=team2cocapt)
        curr_temp_team2.save()

    ### BUILD THE TEAMS DATA
    seasonData = Team.objects.values().filter(season_id__name=newstate.season)
    seasonInfo = Season.objects.values('name','description','master_win__handle','gold_win__handle','silver_win__handle','bronze_win__handle').filter(name=newstate.season)
    teamInfo = season(seasonInfo[0])
    try:
        teamInfo.setTeams(TeamWins.objects.values('team_name').filter(match_date__gte=request.session['start_date'], match_date__lte=request.session['end_date']).distinct())
        dates = TeamWins.objects.values('match_date').filter(match_date__gte=request.session['start_date'], match_date__lte=request.session['end_date']).distinct()
        for date in dates:
            teamInfo.addMatches(TeamWins.objects.values().filter(match_date=date['match_date']).order_by('map'))
        teamInfo.calcWins()
        for match in teamInfo.match:
            for round in match.round:
                teamInfo.maps.append(round.map)
    except:
        teamInfo.setTeams(Team.objects.values().filter(season_id__name=newstate.season).annotate(team_name=F('name'))) 
    teamInfo.addMapRating(teamInfo.maps)

    teamInfo.set_player_list(request,teamInfo.team1,1)
    teamInfo.set_player_list(request,teamInfo.team2,2)
    teamInfo.team1performance = teamInfo.team1seasonkdr - teamInfo.team1startkdr
    teamInfo.team2performance = teamInfo.team2seasonkdr - teamInfo.team2startkdr
    teamInfo.team1advantage = teamInfo.team1startkdr - teamInfo.team2startkdr
    teamInfo.team2advantage = teamInfo.team2startkdr - teamInfo.team1startkdr
    teamInfo.team1capt = Team.objects.values('captain_id').filter(name=teamInfo.team1)
    teamInfo.team1cocapt = Team.objects.values('co_captain_id').filter(name=teamInfo.team1)
    teamInfo.team2capt = Team.objects.values('captain_id').filter(name=teamInfo.team2)
    teamInfo.team2cocapt = Team.objects.values('co_captain_id').filter(name=teamInfo.team2)

    win_data = SeasonWins.objects.values('match_date','match_id','map','round_id','win_side','season','winner').filter(match_date__gte=request.session['start_date'], match_date__lte=request.session['end_date'])

    Team1Geeks = Geek.objects.values('geek_id','handle').filter(alltime_kdr__gte=0).order_by('alltime_kdr')
    for i in Team1Geeks:
        for j in teamInfo.team1players:
            if j.name == i['handle']:
                i['selected'] = 1

    Team2Geeks = Geek.objects.values('geek_id','handle').filter(alltime_kdr__gte=0).order_by('alltime_kdr')
    for i in Team2Geeks:
        for j in teamInfo.team2players:
            if j.name == i['handle']:
                i['selected'] = 1
    teamInfo.geekidlist = [geek.id for geek in teamInfo.team1players]
    teamInfo.geekidlist+=[geek.id for geek in teamInfo.team2players]

       

    context = {'gfgames':teamInfo,
                'rounds':win_data,
                'geeks1':Team1Geeks,
                'geeks2':Team2Geeks,
                'tab':tab,
#               'players': players, 
#               'games': games,
               'title': 'GeekFest Teams',
               'stateinfo': zip(mainmenu.menu,mainmenu.page,mainmenu.state),
            #    'eventdates':request.session['eventdates'],
               'state':newstate,
               }
    return HttpResponse(template.render(context, request))

#  ███████████ █████ ██████████ ███████████    █████████ 
# ░█░░░███░░░█░░███ ░░███░░░░░█░░███░░░░░███  ███░░░░░███
# ░   ░███  ░  ░███  ░███  █ ░  ░███    ░███ ░███    ░░░ 
#     ░███     ░███  ░██████    ░██████████  ░░█████████ 
#     ░███     ░███  ░███░░█    ░███░░░░░███  ░░░░░░░░███
#     ░███     ░███  ░███ ░   █ ░███    ░███  ███    ░███
#     █████    █████ ██████████ █████   █████░░█████████ 
#    ░░░░░    ░░░░░ ░░░░░░░░░░ ░░░░░   ░░░░░  ░░░░░░░░░  
                                                       
                                                       
                                                       
def tiers(request):
    mainmenu.set('Tiers')
    context={}
    template = 'tiers.html'
    if 'datetype' not in request.session:
        request.session['datetype'] = 'season'
    newstate.setsession(request.session['start_date'],request.session['end_date'],'',0,'Tiers', request.session['selector'],request.session['datetype'])
    context['title'] = 'GeekFest Tiers'
    context['stateinfo'] = zip(mainmenu.menu,mainmenu.page,mainmenu.state)
    print(mainmenu.menu,mainmenu.page,mainmenu.state)
    context['state'] = newstate
    context['players'] = TiersData.objects.values('geekid','player','tier','tier_id','year_kdr','alltime_kdr').filter(matchdate__gte=request.session['start_date'], matchdate__lte=request.session['end_date']).order_by('-kdr__avg').annotate(Avg('kdr'),Sum('kills'),Sum('deaths'),Sum('assists'),Avg('akdr'))
    context['tier0'] = list(filter(lambda tiers: tiers['tier_id'] == 1, list(context['players'])))
    context['tier1'] = list(filter(lambda tiers: tiers['tier_id'] == 2, list(context['players'])))
    context['tier2'] = list(filter(lambda tiers: tiers['tier_id'] == 3, list(context['players'])))
    context['tier3'] = list(filter(lambda tiers: tiers['tier_id'] == 4, list(context['players'])))
    
    weapons_list = FragDetails.objects.values('killer', 'weapon').filter(match_date__gte=request.session['start_date'], match_date__lte=request.session['end_date'], type='kill').annotate(Count('weapon')).order_by('-weapon__count')

    for geek in context['players']:
        try:
            geek['diffkdr'] = geek['kdr__avg'] - geek['year_kdr']
        except:
            geek['diffkdr'] = 'n/a'
        try:
            geek['new_kdr'] = geek['kills__sum'] / geek['deaths__sum']
        except:
            geek['new_kdr'] = 'n/a'
        high = 0
        for item in weapons_list:
            if item['killer'] == geek['player']:
                if item['weapon__count'] > high:
                    geek['weapon'] = item
                    high = item['weapon__count']

        # geek['weapon'] = FragDetails.objects.values('weapon').filter(killer=geek['player'],match_date__gte=request.session['start_date'], match_date__lte=request.session['end_date'], type='kill').annotate(Count('weapon')).order_by('-weapon__count')[0]
        # print(FragDetails.objects.values('weapon').filter(killer=geek['player'],match_date__gte=request.session['start_date'], match_date__lte=request.session['end_date'], type='kill').annotate(Count('weapon')).order_by('-weapon__count').query)


    return render(request, template, context)

##### GEEKFEST XX: VIRTUAL CODE ######
# def gfxx(request):
#     mainmenu.set('Event')
#     template = loader.get_template('gfxxv.html')
#     newstate.setsession('2020-12-02','2020-12-02','',0,'Event', request.session['selector'])

#     players = func.get_stats_data(newstate)
#     players.sort(key=lambda players: players.kdr_v_avg, reverse=True)
#     print(players[0])
#     v_avg=[players[0],players[-1]]
    
#     players.sort(key=lambda players: players.kdr, reverse=True)
     
#     tier0 = [x for x in players if x.tier == 0]
#     tier1 = [x for x in players if x.tier == 1]
#     tier2 = [x for x in players if x.tier == 2]
#     tier3 = [x for x in players if x.tier == 3]

#     newstate.value = 'event'
#     award_types, awards = func.get_awards(newstate)
    

#     context = {'tier0':tier0, 'tier1': tier1, 'tier2': tier2, 'tier3':tier3, 'players':players, 'v_avg': v_avg,
#                'awards': awards, 'types':award_types,
#                'title': 'GeekFest Tiers',
#                'stateinfo': zip(mainmenu.menu,mainmenu.state),
#                'eventdates':request.session['eventdates'],
#                'state':newstate,
#                }
#     return HttpResponse(template.render(context, request))

def list_builder(data,element):
    data = sorted(data, key=lambda g: g[element])
    dataList = []
    key_func = lambda x: x[element]
    for key, group in groupby(data, key_func):
        try:
            if key[:3] != 'BOT' and key != 'n/a':
                dataList.append({'item': key, 'count':len([ele for ele in (list(group)) if isinstance(ele,dict)])})
        except:
            dataList.append({'item': key, 'count':len([ele for ele in (list(group)) if isinstance(ele,dict)])})

    # result = [m for m in fragList if 'de_cbble' in m]
    result = sorted(dataList, key=lambda g: g['count'])
    return(result)

def item_getter(data,item):
    itemList = list(filter(lambda n: n['item'] == item, data))
    if itemList:
        return(itemList[0]['count'])
    else:
        return(0)

#  ██████   ██████   █████████   ███████████   █████████ 
# ░░██████ ██████   ███░░░░░███ ░░███░░░░░███ ███░░░░░███
#  ░███░█████░███  ░███    ░███  ░███    ░███░███    ░░░ 
#  ░███░░███ ░███  ░███████████  ░██████████ ░░█████████ 
#  ░███ ░░░  ░███  ░███░░░░░███  ░███░░░░░░   ░░░░░░░░███
#  ░███      ░███  ░███    ░███  ░███         ███    ░███
#  █████     █████ █████   █████ █████       ░░█████████ 
# ░░░░░     ░░░░░ ░░░░░   ░░░░░ ░░░░░         ░░░░░░░░░  
                                                       

def maps(request):
    mainmenu.set('Maps')
    template = loader.get_template('maps.html')
    newstate.setsession(request.session['start_date'],request.session['end_date'],'',0,'Maps', request.session['selector'],request.session['datetype'])
    # print(newstate.seasons)    

    newstate.compare = 'map'
    #TiersData.objects.values('player').filter(tier="Gold", matchdate__gte=request.session['start_date'], matchdate__lte=request.session['end_date']).order_by('-kdr__avg').annotate(Avg('kdr')) 
    endDate = datetime.datetime.strptime(request.session['end_date'], '%Y-%m-%d') + datetime.timedelta(days=1)
    rounds = MatchRound.objects.prefetch_related('match').filter(match__match_date__gte=request.session['start_date'], match__match_date__lte=endDate.strftime('%Y-%m-%d %H:%M:%S'))

    killData = Frag.objects.prefetch_related('geek').prefetch_related('round__match').filter(round__in=rounds, is_teamkill=False, geek__is_member=True).values('round__match__map', 'geek__handle', 'geek_id', 'round__match__match_date').annotate(num_frags=Count('frag_id')).order_by('round__match__match_date', '-num_frags')
    
    deathData = Death.objects.prefetch_related('geek').prefetch_related('round__match').filter(round__in=rounds, is_teamkill=False, geek__is_member=True).values('round__match__map', 'geek__handle', 'geek_id').annotate(num_deaths=Count('death_id')).order_by('round__match__map')
    
    # print(playData)
    mapGroupData = {}

    for k in killData:
        if (not k['round__match__map'] in mapGroupData):
            mapGroupData[k['round__match__map']] = {
                'map' : k['round__match__map'],
                'player_info' : {}
            }
        mapGroupData[k['round__match__map']]['player_info'][k['geek_id']] = {
            'player': k['geek__handle'],
            'id': k['geek_id'],
            'kills': k['num_frags'],
            'deaths': 0,
            'kdr': k['num_frags']
            }

    for d in deathData:
        if (not d['round__match__map'] in mapGroupData):
            continue
        if (not d['geek_id'] in mapGroupData[d['round__match__map']]['player_info']):
            mapGroupData[d['round__match__map']]['player_info'][d['geek_id']] = {
                'player': d['geek__handle'],
                'id': d['geek_id'],
                'kills': 0,
                'deaths': 0,
                'buys': 0
            }
        curPlayer = mapGroupData[d['round__match__map']]['player_info'][d['geek_id']]
        curPlayer['deaths'] = d['num_deaths']
        if (d['num_deaths'] > 0):
            curPlayer['kdr'] = curPlayer['kills']/curPlayer['deaths']
        curPlayer['kdr'] = round(curPlayer['kdr'], 2)

    ###########  Add the map win % and rating  ###################
    map_data = (MapData.objects.values('map_id','map','win_side','type','theme','votescore','thumbnail').annotate(wins=Count('win_side')).filter(match_date__gte=request.session['start_date'], match_date__lte=endDate.strftime('%Y-%m-%d')))
    map_plays = (SeasonMatch.objects.values('map').annotate(plays=Count('match_id')))


    map_data_list = []
    last_map = ''
    curr_rec = {}
    for i in map_data:
        curr_map = i['map']
        if i['map'] == last_map:
            if curr_rec['win_side'] == 'CT' and i['win_side'] == 'TERRORIST':
                curr_rec['other_side'] = i['wins']
            else:
                curr_rec['other_side'] = curr_rec['wins']
                curr_rec['win_side'] = 'CT'
                curr_rec['wins'] = i['wins']
            curr_rec['CT_win_pct'] = (curr_rec['wins'] / (curr_rec['other_side'] + curr_rec['wins']))*100
        else:
            if len(curr_rec) > 0:
                map_data_list.append(curr_rec)
            curr_rec = i
        last_map = i['map']
    map_data_list.append(curr_rec)
    print(map_data_list)

    for i in mapGroupData:
        for j in map_data_list:
            if i == j['map']:
                mapGroupData[i]['ct_win_pct'] = j['CT_win_pct']
                mapGroupData[i]['rating'] = j['votescore']
                mapGroupData[i]['id'] = j['map_id']
                mapGroupData[i]['thumb'] = j['thumbnail']
        for k in map_plays:
            if i == k['map']:
                mapGroupData[i]['plays'] = k['plays']

    context = {'title': 'GeekFest Maps', 
               'stateinfo': zip(mainmenu.menu,mainmenu.page,mainmenu.state),
               'state':newstate,
               'mapstats':mapGroupData.values,
               }
    return HttpResponse(template.render(context, request))

# ███╗   ███╗ █████╗ ██████╗ ███████╗    ██████╗ ███████╗████████╗ █████╗ ██╗██╗     ███████╗
# ████╗ ████║██╔══██╗██╔══██╗██╔════╝    ██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║██║     ██╔════╝
# ██╔████╔██║███████║██████╔╝███████╗    ██║  ██║█████╗     ██║   ███████║██║██║     ███████╗
# ██║╚██╔╝██║██╔══██║██╔═══╝ ╚════██║    ██║  ██║██╔══╝     ██║   ██╔══██║██║██║     ╚════██║
# ██║ ╚═╝ ██║██║  ██║██║     ███████║    ██████╔╝███████╗   ██║   ██║  ██║██║███████╗███████║
# ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝    ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝
                                                                                           
def mapdetails(request):
    mainmenu.set('Map Details')
    template = loader.get_template('mapdetails.html')
    newstate.setsession(request.session['start_date'],request.session['end_date'],'',0,'Map Details', request.session['selector'],request.session['datetype'])
    # print(newstate.seasons)    

    newstate.compare = 'map'
    #TiersData.objects.values('player').filter(tier="Gold", matchdate__gte=request.session['start_date'], matchdate__lte=request.session['end_date']).order_by('-kdr__avg').annotate(Avg('kdr')) 
    endDate = datetime.datetime.strptime(request.session['end_date'], '%Y-%m-%d') + datetime.timedelta(days=1)
    rounds = MatchRound.objects.prefetch_related('match').filter(match__match_date__gte=request.session['start_date'], match__match_date__lte=endDate.strftime('%Y-%m-%d %H:%M:%S'))

    killData = Frag.objects.prefetch_related('geek').prefetch_related('round__match').filter(round__in=rounds, is_teamkill=False, geek__is_member=True).values('round__match__map', 'geek__handle', 'geek_id', 'round__match__match_date').annotate(num_frags=Count('frag_id')).order_by('round__match__match_date', '-num_frags')
    
    deathData = Death.objects.prefetch_related('geek').prefetch_related('round__match').filter(round__in=rounds, is_teamkill=False, geek__is_member=True).values('round__match__map', 'geek__handle', 'geek_id').annotate(num_deaths=Count('death_id')).order_by('round__match__map')
    
    # print(playData)
    mapGroupData = {}

    for k in killData:
        if (not k['round__match__map'] in mapGroupData):
            mapGroupData[k['round__match__map']] = {
                'map' : k['round__match__map'],
                'player_info' : {}
            }
        mapGroupData[k['round__match__map']]['player_info'][k['geek_id']] = {
            'player': k['geek__handle'],
            'id': k['geek_id'],
            'kills': k['num_frags'],
            'deaths': 0,
            'kdr': k['num_frags']
            }

    for d in deathData:
        if (not d['round__match__map'] in mapGroupData):
            continue
        if (not d['geek_id'] in mapGroupData[d['round__match__map']]['player_info']):
            mapGroupData[d['round__match__map']]['player_info'][d['geek_id']] = {
                'player': d['geek__handle'],
                'id': d['geek_id'],
                'kills': 0,
                'deaths': 0,
                'buys': 0
            }
        curPlayer = mapGroupData[d['round__match__map']]['player_info'][d['geek_id']]
        curPlayer['deaths'] = d['num_deaths']
        if (d['num_deaths'] > 0):
            curPlayer['kdr'] = curPlayer['kills']/curPlayer['deaths']
        curPlayer['kdr'] = round(curPlayer['kdr'], 2)

    ###########  Add the map win % and rating  ###################
    map_data = (MapData.objects.values('map','win_side','type','theme','votescore').annotate(wins=Count('win_side')))
    map_plays = (SeasonMatch.objects.values('map').annotate(plays=Count('match_id')))


    map_data_list = []
    last_map = ''
    curr_rec = {}
    for i in map_data:
        curr_map = i['map']
        if i['map'] == last_map:
            if curr_rec['win_side'] == 'CT' and i['win_side'] == 'TERRORIST':
                curr_rec['other_side'] = i['wins']
            else:
                curr_rec['other_side'] = curr_rec['wins']
                curr_rec['win_side'] = 'CT'
                curr_rec['wins'] = i['wins']
            curr_rec['CT_win_pct'] = (curr_rec['wins'] / (curr_rec['other_side'] + curr_rec['wins']))*100
        else:
            if len(curr_rec) > 0:
                map_data_list.append(curr_rec)
            curr_rec = i
        last_map = i['map']
    map_data_list.append(curr_rec)

    for i in mapGroupData:
        for j in map_data_list:
            if i == j['map']:
                mapGroupData[i]['ct_win_pct'] = j['CT_win_pct']
                mapGroupData[i]['rating'] = j['votescore']
        for k in map_plays:
            if i == k['map']:
                mapGroupData[i]['plays'] = k['plays']

    #####  NEW MAP CONTENT ####
    # NEW API LOGIC:  https://www.agiliq.com/blog/2019/04/drf-polls/

    MapList = []

    dataMap = Maps.objects.values('idmap','map','description','workshop_link','type','theme','votescore', 'metascore','votes','ct_wins','t_wins','plays','s_plays','last_play','hero_image','radar','thumbnail','image2','image3','no_obj_rounds', 'bomb_plant_rounds', 'bomb_explode_rounds', 'defuse_rounds')
    dataFrag = FragDetails.objects.values('match_date','killer','victim','map','weapon','type').filter(type='kill')
    if request.user.is_authenticated:
        current_user = request.user
        userid = Geek.objects.values('geek_id').filter(userid=current_user.id)[0]['geek_id']
        dataRating = MapRating.objects.annotate(count=F('rating'), item=F('map__map')).values('item', 'count').filter(geek__userid=current_user.id)
        print(dataRating)
    else:
        userid = 'none'
    themes = list_builder(dataMap,'theme')

    for j in dataMap:
        MapList.append(map_summary(j))
    
    for m in MapList:
        dataRec = list(filter(lambda dat: dat['map'] == m.name, list(dataFrag)))
        m.players = list_builder(dataRec,'killer')
        m.weapons = list_builder(dataRec,'weapon')
        for w in m.weapons:
            m.kills += w['count']
        m.knives = item_getter(m.weapons,'Knife') + item_getter(m.weapons, 'knife_karambit')+ item_getter(m.weapons, 'knife_butterfly')
        m.grenades = item_getter(m.weapons,'hegrenade')
        m.flames = item_getter(m.weapons,'inferno')
        m.tazes = item_getter(m.weapons,'taser')
        m.snipes = item_getter(m.weapons,'awp') + item_getter(m.weapons,'g3sg1') + item_getter(m.weapons,'scar20') + item_getter(m.weapons,'ssg08')
        m.snipe_pct = round(m.snipes / m.kills,2)*100 if m.kills > 0 else 0
        m.hmg = item_getter(m.weapons,'Yakospray') + item_getter(m.weapons,'m249')
        m.hmg_pct = round(m.hmg / m.kills,2)*100 if m.kills > 0 else 0
        if m.plays:
            m.ninja = int(round((m.knives + m.grenades + m.flames + m.tazes) / m.plays,0))
        m.ninja_pct = round(m.ninja / m.kills,2)*100 if m.kills > 0 else 0
        if request.user.is_authenticated:
            m.geek_rating = item_getter(dataRating,m.name)

    context = {'title': 'GeekFest Maps', 
               'stateinfo': zip(mainmenu.menu,mainmenu.page,mainmenu.state),
               'maps':MapList,
               'state':newstate,
               'mapstats':mapGroupData.values,
               'userid':userid,
            #    'playdata':playData
               }
    return HttpResponse(template.render(context, request))







# ███╗   ███╗ █████╗ ██████╗ ███████╗    ███████╗██╗   ██╗███╗   ███╗███╗   ███╗ █████╗ ██████╗ ██╗   ██╗
# ████╗ ████║██╔══██╗██╔══██╗██╔════╝    ██╔════╝██║   ██║████╗ ████║████╗ ████║██╔══██╗██╔══██╗╚██╗ ██╔╝
# ██╔████╔██║███████║██████╔╝███████╗    ███████╗██║   ██║██╔████╔██║██╔████╔██║███████║██████╔╝ ╚████╔╝ 
# ██║╚██╔╝██║██╔══██║██╔═══╝ ╚════██║    ╚════██║██║   ██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██╔══██╗  ╚██╔╝  
# ██║ ╚═╝ ██║██║  ██║██║     ███████║    ███████║╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║██║  ██║   ██║   
# ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝    ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                                                                                                       


def map2(request):
    mainmenu.set('Maps')
    template = loader.get_template('mapsummary.html')
    newstate.setsession(request.session['start_date'],request.session['end_date'],'',0,'Map Summary', request.session['selector'],request.session['datetype'])
    mid = request.session['mapid']
    # print(newstate.seasons)    
    # if request.method == 'POST':
    #     print('running post request')
    #     mid = request.POST.get('mid')
    #     map_update = Maps.objects.get(idmap=mid)
    #     print(map_update)
    #     map_update.hero_image = request.FILES.get('image') 
    #     # print(dataMap[0])
    #     map_update.save()

    newstate.compare = 'map'
    #TiersData.objects.values('player').filter(tier="Gold", matchdate__gte=request.session['start_date'], matchdate__lte=request.session['end_date']).order_by('-kdr__avg').annotate(Avg('kdr')) 
    endDate = datetime.datetime.strptime(request.session['end_date'], '%Y-%m-%d') + datetime.timedelta(days=1)
    MapList = []

    dataMap = Maps.objects.values('idmap','map','description','workshop_link','type','theme','votescore', 'metascore','votes','ct_wins','t_wins','plays','s_plays','last_play','hero_image','radar','thumbnail','image2','image3','no_obj_rounds', 'bomb_plant_rounds', 'bomb_explode_rounds', 'defuse_rounds') \
        .filter(idmap=mid)
    dataFrag = FragDetails.objects.values('match_date','killer','victim','map','weapon','type').filter(type='kill')


    if request.user.is_authenticated:
        current_user = request.user
        userid = Geek.objects.values('geek_id').filter(userid=current_user.id)[0]['geek_id']
        dataRating = MapRating.objects.annotate(count=F('rating'), item=F('map__map')).values('item', 'count').filter(geek__userid=current_user.id)
        # print(dataRating)
    else:
        userid = 'none'
    themes = list_builder(dataMap,'theme')

    for j in dataMap:
        MapList.append(map_summary(j))
    
    for m in MapList:
        dataRec = list(filter(lambda dat: dat['map'] == m.name, list(dataFrag)))
        m.players = list_builder(dataRec,'killer')
        m.weapons = list_builder(dataRec,'weapon')
        m.matches = list_builder(dataRec, 'match_date')
        for w in m.weapons:
            m.kills += w['count']
        m.knives = item_getter(m.weapons,'Knife') + item_getter(m.weapons, 'knife_karambit')+ item_getter(m.weapons, 'knife_butterfly')
        m.grenades = item_getter(m.weapons,'hegrenade')
        m.flames = item_getter(m.weapons,'inferno')
        m.tazes = item_getter(m.weapons,'taser')
        m.snipes = item_getter(m.weapons,'awp') + item_getter(m.weapons,'g3sg1') + item_getter(m.weapons,'scar20') + item_getter(m.weapons,'ssg08')
        m.snipe_pct = round(m.snipes / m.kills,2)*100 if m.kills > 0 else 0
        m.hmg = item_getter(m.weapons,'Yakospray') + item_getter(m.weapons,'m249')
        m.hmg_pct = round(m.hmg / m.kills,2)*100 if m.kills > 0 else 0
        if m.plays:
            m.ninja = int(round((m.knives + m.grenades + m.flames + m.tazes) / m.plays,0))
        m.ninja_pct = round(m.ninja / m.kills,2)*100 if m.kills > 0 else 0
        if request.user.is_authenticated:
            m.geek_rating = item_getter(dataRating,m.name)

    # print(MapList[0])

    context = {'title': 'GeekFest Maps', 
               'stateinfo': zip(mainmenu.menu,mainmenu.page,mainmenu.state),
               'maps':MapList[0],
               'state':newstate,
            #    'mapstats':mapGroupData.values,
               'userid':userid,
            #    'playdata':playData
               }
    return HttpResponse(template.render(context, request))



#  █████   ███   █████ ██████████   █████████   ███████████     ███████    ██████   █████  █████████ 
# ░░███   ░███  ░░███ ░░███░░░░░█  ███░░░░░███ ░░███░░░░░███  ███░░░░░███ ░░██████ ░░███  ███░░░░░███
#  ░███   ░███   ░███  ░███  █ ░  ░███    ░███  ░███    ░███ ███     ░░███ ░███░███ ░███ ░███    ░░░ 
#  ░███   ░███   ░███  ░██████    ░███████████  ░██████████ ░███      ░███ ░███░░███░███ ░░█████████ 
#  ░░███  █████  ███   ░███░░█    ░███░░░░░███  ░███░░░░░░  ░███      ░███ ░███ ░░██████  ░░░░░░░░███
#   ░░░█████░█████░    ░███ ░   █ ░███    ░███  ░███        ░░███     ███  ░███  ░░█████  ███    ░███
#     ░░███ ░░███      ██████████ █████   █████ █████        ░░░███████░   █████  ░░█████░░█████████ 
#      ░░░   ░░░      ░░░░░░░░░░ ░░░░░   ░░░░░ ░░░░░           ░░░░░░░    ░░░░░    ░░░░░  ░░░░░░░░░  
                                                                                                   
                                                                                                   
                                                                                                   
def weapons(request):
    mainmenu.set('Weapons')
    template = loader.get_template('weapons.html')
    newstate.setsession(request.session['start_date'],request.session['end_date'],'',0,'Weapons', request.session['selector'],request.session['datetype'])

    endDate = datetime.datetime.strptime(request.session['end_date'], '%Y-%m-%d') + datetime.timedelta(days=1)
    rounds = MatchRound.objects.prefetch_related('match').filter(match__match_date__gte=request.session['start_date'], match__match_date__lte=endDate.strftime('%Y-%m-%d %H:%M:%S'))

    killData = Frag.objects.prefetch_related('geek').prefetch_related('item').filter(round__in=rounds, is_teamkill=False, geek__is_member=True).values('item__name', 'geek__handle', 'item__decscription', 'geek_id').annotate(num_frags=Count('frag_id')).order_by('item__decscription', '-num_frags')
    deathData = Death.objects.prefetch_related('geek').prefetch_related('item').filter(round__in=rounds, is_teamkill=False,  geek__is_member=True).values('item__name', 'geek__handle', 'item__decscription', 'geek_id').annotate(num_deaths=Count('death_id')).order_by('item__decscription')
    buyData = Buy.objects.prefetch_related('geek').prefetch_related('item').filter(round__in=rounds).values('item__name', 'geek__handle', 'item__decscription', 'geek_id').annotate(num_buys=Count('buy_id')).order_by('item__decscription')

    itemGroupedData = {}

    for k in killData:
        if (not k['item__decscription'] in itemGroupedData):
            itemGroupedData[k['item__decscription']] = {
                'item_name' : k['item__name'],
                'item_description' : k['item__decscription'],
                'player_info' : {}
            }

        itemGroupedData[k['item__decscription']]['player_info'][k['geek_id']] = {
            'player': k['geek__handle'],
            'id': k['geek_id'],
            'kills': k['num_frags'],
            'deaths': 0,
            'buys': 0
        }

    for d in deathData:
        if (not d['item__decscription'] in itemGroupedData):
            continue
        if (not d['geek_id'] in itemGroupedData[d['item__decscription']]['player_info']):
            itemGroupedData[d['item__decscription']]['player_info'][d['geek_id']] = {
                'player': d['geek__handle'],
                'id': d['geek_id'],
                'kills': 0,
                'deaths': 0,
                'buys': 0
            }
        itemGroupedData[d['item__decscription']]['player_info'][d['geek_id']]['deaths'] = d['num_deaths']

    for b in buyData:
        if (not b['item__decscription'] in itemGroupedData):
            continue
        if (not b['geek_id'] in itemGroupedData[b['item__decscription']]['player_info']):
            #itemGroupedData[b['item__decscription']]['player_info'][b['geek_id']] = {
            #    'player': b['geek__handle'],
            #    'id': b['geek_id'],
            #    'kills': 0,
            #    'deaths': 0,
            #    'buys': 0
            #}
            #for now, only show if geek was killed by or killed with a weapon, maybe show buys later
            continue
        itemGroupedData[b['item__decscription']]['player_info'][b['geek_id']]['buys'] = b['num_buys']

    newstate.compare = 'weapon'
    context = {'weapons': itemGroupedData.values,
               'title': 'GeekFest Weapons',
               'state':newstate,
               'stateinfo': zip(mainmenu.menu,mainmenu.page,mainmenu.state), }
    return HttpResponse(template.render(context, request))

#    █████████  ██████████ ██████████ █████   ████  █████████ 
#   ███░░░░░███░░███░░░░░█░░███░░░░░█░░███   ███░  ███░░░░░███
#  ███     ░░░  ░███  █ ░  ░███  █ ░  ░███  ███   ░███    ░░░ 
# ░███          ░██████    ░██████    ░███████    ░░█████████ 
# ░███    █████ ░███░░█    ░███░░█    ░███░░███    ░░░░░░░░███
# ░░███  ░░███  ░███ ░   █ ░███ ░   █ ░███ ░░███   ███    ░███
#  ░░█████████  ██████████ ██████████ █████ ░░████░░█████████ 
#   ░░░░░░░░░  ░░░░░░░░░░ ░░░░░░░░░░ ░░░░░   ░░░░  ░░░░░░░░░  
                                                            
def geeks(request):
    ### INITIALIZE THE PAGE AND SESSION DATA
    mainmenu.set('Geeks')
    template = loader.get_template('geeks.html')
    newstate.setsession(request.session['start_date'],request.session['end_date'],'',0,'Geeks', request.session['selector'],request.session['datetype'])

    if request.GET.get('code'):
        Geek.objects.filter(geek_code=(request.GET.get('code'))).update(validated=1, geek_code='validated')    
        return redirect("/accounts/login")            
            


    ### BUILD GEEK DATA
    geekData = GeekInfo.objects.values().order_by('-tenure')
    seasonWinners = list(Season.objects.values('name','master_win','gold_win','silver_win','bronze_win'))

    ### CALC ANY SEASON AWARDS
    raw_award_data = GeekfestMatchAward.objects.select_related('match', 'season', 'geekfest_award', 'geekfest_award__award_category', 'geek').filter(geekfest_award__award_title='Colonel Sanders').values(
        'geek__handle', 'geekfest_award__award_name', 'geekfest_award__award_title', 'geekfest_award__award_category__category_name',
        'geekfest_award__award_image_path', 'geekfest_award__award_description', 'geekfest_award__award_value_type', 'match_id__season_id__name',
        'geekfest_award__award_category__category_color','geekfest_award__award_category__award_category_id').annotate(
            max_points=Max('award_value'), sum_points=Sum('award_value'), min_points=Min('award_value')).order_by(
                "match_id__season_id", "-sum_points")

    curr_season = ""
    award_winners = []
    for row in raw_award_data:
        if curr_season != row['match_id__season_id__name']:
            curr_season = row['match_id__season_id__name']
            award_winners.append([row['geek__handle'], row['sum_points'], row['match_id__season_id__name']])

    context = {'geeks': geekData,
               'title': 'GeekFest Geeks',
               'awards': award_winners,
               'winners': seasonWinners,
               'state':newstate,
               'stateinfo': zip(mainmenu.menu,mainmenu.page,mainmenu.state),
               }
    return HttpResponse(template.render(context, request))

#  ███████████  ████                                             ██████████             █████               ███  ████         
# ░░███░░░░░███░░███                                            ░░███░░░░███           ░░███               ░░░  ░░███         
#  ░███    ░███ ░███   ██████   █████ ████  ██████  ████████     ░███   ░░███  ██████  ███████    ██████   ████  ░███   █████ 
#  ░██████████  ░███  ░░░░░███ ░░███ ░███  ███░░███░░███░░███    ░███    ░███ ███░░███░░░███░    ░░░░░███ ░░███  ░███  ███░░  
#  ░███░░░░░░   ░███   ███████  ░███ ░███ ░███████  ░███ ░░░     ░███    ░███░███████   ░███      ███████  ░███  ░███ ░░█████ 
#  ░███         ░███  ███░░███  ░███ ░███ ░███░░░   ░███         ░███    ███ ░███░░░    ░███ ███ ███░░███  ░███  ░███  ░░░░███
#  █████        █████░░████████ ░░███████ ░░██████  █████        ██████████  ░░██████   ░░█████ ░░████████ █████ █████ ██████ 
# ░░░░░        ░░░░░  ░░░░░░░░   ░░░░░███  ░░░░░░  ░░░░░        ░░░░░░░░░░    ░░░░░░     ░░░░░   ░░░░░░░░ ░░░░░ ░░░░░ ░░░░░░  
#                                ███ ░███                                                                                     
#                               ░░██████                                                                                      
#                                ░░░░░░                                                                                       

def playerdetails(request):

    ### INITIALIZE THE PAGE AND SESSION DATA
    mainmenu.set('Geeks')
    template = loader.get_template('playerdetails.html')
    pid = request.session['playerid']

    newstate.setsession(request.session['start_date'],request.session['end_date'],'',request.session['playerid'],'PlayerDetails', request.session['selector'],request.session['datetype'])
    request.session['page'] = newstate.page

    ### SETUP VALIDATION LOGIC FOR REGISTERED PLAYERS
    try:
        geek = GeekAuthUser.objects.values('geek_id','handle','valid_sent_date','validated','username','first_name','email','member_since').filter(geek_id=pid) 
    except:
        print('player not logged')
    if request.GET.get('claim'):
        claim = request.GET.get('claim')
        if claim == 'claim' or claim == 'resend':
            geek_code = uuid.uuid4()
            password = geek[0]['first_name']+geek[0]['member_since'].strftime('%m%Y')
            # httplink = 'http://192.168.0.156:8000/Geeks?code='+str(geek_code)
            httplink = 'http://stats.geekfestclan.com/Geeks?code='+str(geek_code)
            # Players.objects.filter(username=request.user.id).update(last_seen=datetime.now())
            Geek.objects.filter(geek_id=pid).update(valid_sent_date=date.today(), validated=0, geek_code=str(geek_code))
            # print(geek[0]['handle'])
            send_mail(
                'Welcome to The GeekFest',
                'Your GeekFest Player name '+str(geek[0]['username'])+' has been claimed.  Your password is: '+password+' Click on this link to validate your email and login:  '+httplink,
                'bot.geekfest@gmail.com',
                [str(geek[0]['email'])],
                fail_silently=False,)

            # print('send email')
            
        elif claim == 'resend': 
            print('resend email')

    ### BUILD THE PLAYER DETAIL DATA
    psumm = (TiersData.objects.values('geekid','player','tier','alltime_kdr','year_kdr','last90_kdr')
                      .filter(geekid=pid,matchdate__gte=request.session['start_date'], matchdate__lte=request.session['end_date'])
                      .annotate(Avg('kdr'),Sum('kills'),Sum('deaths'),Sum('assists'),Avg('akdr')))
    playerData = player(psumm)


    if playerData.name == 'No data':
        playerData.nemesis = 'There is no player data for this date.  Please select a date when this player played.'
    else:
        pdata = (FragDetails.objects.values('id','match_date','killer','victim','victim_id','map','weapon','type')
                     .filter(Q (id=pid) | Q(victim_id=pid),match_date__gte=request.session['start_date'], match_date__lte=request.session['end_date'])
                     .order_by('id','type'))
        
        endDate = datetime.datetime.strptime(request.session['end_date'], '%Y-%m-%d') + datetime.timedelta(days=1)
        ddata = (Damage.objects.select_related('round', 'geek', 'round__match', 'item')
                 .filter(geek_id=pid,round__match__match_date__gte=request.session['start_date'], round__match__match_date__lte=endDate.strftime('%Y-%m-%d %H:%M:%S'))
                .values('geek__handle', 'damage_armor', 'damage_health', 'armor_remaining', 'health_remaining', 'hitgroup', 'item__name', 'is_team_damage', 'is_kill')
                .order_by('hitgroup'))

        # lst = list(pdata.all())
        kdata = list(filter(lambda p: p['type'] == 'kill', list(pdata)))
        laplayer = list(filter(lambda p: p['type'] == 'assist', list(pdata)))
        lkplayer = list(filter(lambda w: str(w['id']) == pid, list(kdata)))
        lvplayer = list(filter(lambda w: str(w['victim_id']) == pid, list(kdata)))

        headData = list(filter(lambda p: p['hitgroup'] == 'head', list(ddata)))
        chestData = list(filter(lambda p: p['hitgroup'] == 'chest', list(ddata)))
        hitdata = {}
        
        for hitgroup, hits in groupby(list(ddata), lambda dm: dm['hitgroup']):
            hitdata[hitgroup] = list(hits)
        

        playerData.addWeapons('killer','weapon',listbuilder(lkplayer,'weapon'))
        playerData.addWeapons('victim','weapon',listbuilder(lvplayer,'weapon'))
        playerData.addMaps('killer','map',listbuilder(lkplayer,'map'))
        playerData.addMaps('victim','map',listbuilder(lvplayer,'map'))
        playerData.addMaps('assist','map',listbuilder(laplayer,'map'))
        playerData.addOpps('killer','victim',listbuilder(lkplayer,'victim'))
        playerData.addOpps('victim','killer',listbuilder(lvplayer,'killer'))
        playerData.avatar = (Geek.objects.values('avatar').filter(geek_id=playerData.id)[0]['avatar'])

        playerData.calcHitgroups(hitdata)
        playerData.calcStats()
        

    kdr_history = GeekKDRHistory.objects.values('handle','history_date','alltime_kdr','year_kdr','last90_kdr').filter(geek_id=pid).order_by('-history_date')[:10]
    kdr_history = reversed(kdr_history)
    custom_style = Style(background='#d3d3d3',plot_background='#fffaf0', label_font_family='Electrolize', legend_font_size=30, major_label_font_size=20, label_font_size=20, title_font_size=40)
    line_chart = pygal.Line(height=400, legend_at_bottom=True, legend_at_bottom_columns=3, style=custom_style)
    line_chart.title = 'KDR Performance'

    dates = []
    data1 = []
    data2 = []
    data3 = []
    for i in kdr_history:
        data1.append(i['last90_kdr'])
        data2.append(i['year_kdr'])
        data3.append(i['alltime_kdr'])
        dates.append(i['history_date'].strftime('%m-%d'))
    line_chart.x_labels = dates
    line_chart.add('last90',data1)
    line_chart.add('year',data2)
    line_chart.add('alltime',data3)

    
    context = {'player': playerData,
               'geek': geek,
               'data': kdr_history,
               'chart': line_chart.render(disable_xml_declaration=True),
               'title': 'GeekFest Geeks',
               'state':newstate,
               'stateinfo': zip(mainmenu.menu,mainmenu.page,mainmenu.state),
               }
    return HttpResponse(template.render(context, request))

#  ██████████   ██████████ ███████████   █████████   █████ █████        █████████ 
# ░░███░░░░███ ░░███░░░░░█░█░░░███░░░█  ███░░░░░███ ░░███ ░░███        ███░░░░░███
#  ░███   ░░███ ░███  █ ░ ░   ░███  ░  ░███    ░███  ░███  ░███       ░███    ░░░ 
#  ░███    ░███ ░██████       ░███     ░███████████  ░███  ░███       ░░█████████ 
#  ░███    ░███ ░███░░█       ░███     ░███░░░░░███  ░███  ░███        ░░░░░░░░███
#  ░███    ███  ░███ ░   █    ░███     ░███    ░███  ░███  ░███      █ ███    ░███
#  ██████████   ██████████    █████    █████   █████ █████ ███████████░░█████████ 
# ░░░░░░░░░░   ░░░░░░░░░░    ░░░░░    ░░░░░   ░░░░░ ░░░░░ ░░░░░░░░░░░  ░░░░░░░░░  
                                                                                
                                                                                
                                                                                
def details(request):
    ### INITIALIZE THE PAGE AND SESSION DATA
    mainmenu.set('Geeks')
    template = loader.get_template('details.html')
    newstate.setsession(request.session['start_date'],request.session['end_date'],'',request.session['playerid'],'Event Details', request.session['selector'],request.session['datetype'])
    pid = request.session['playerid']
    xOpp = request.session['opponentid']
    xMap = request.session['mapid']
    xWeapon = request.session['weaponid']
    playerName = Geek.objects.values('handle').filter(geek_id=pid)[0]['handle']
    print(playerName)

    ### GET THE DETAILS REQUESTED FROM THE FRAGDETAILS VIEW
    if request.session['opponentid'] != '':
        pdetails = FragDetails.objects.values().filter(id=pid,victim=xOpp,match_date__gte=request.session['start_date'], match_date__lte=request.session['end_date']).order_by('match_datetime')
        details = pdetails.union(FragDetails.objects.values().filter(victim_id=pid,killer=xOpp,match_date__gte=request.session['start_date'], match_date__lte=request.session['end_date']).order_by('match_datetime'),all=True).order_by('match_datetime')
        rType = 'Opponent'
    elif xMap != '':
        pdetails = FragDetails.objects.values().filter(id=pid,map=xMap,match_date__gte=request.session['start_date'], match_date__lte=request.session['end_date']).order_by('match_datetime')
        details = pdetails.union(FragDetails.objects.values().filter(victim_id=pid,map=xMap,match_date__gte=request.session['start_date'], match_date__lte=request.session['end_date']),all=True).order_by('match_datetime')
        rType = 'Map'
    elif xWeapon != '':
        pdetails = FragDetails.objects.values().filter(id=pid,weapon=xWeapon,match_date__gte=request.session['start_date'], match_date__lte=request.session['end_date']).order_by('match_datetime')
        details = pdetails.union(FragDetails.objects.values().filter(victim_id=pid,weapon=xWeapon,match_date__gte=request.session['start_date'], match_date__lte=request.session['end_date']),all=True).order_by('match_datetime')
        rType = 'Weapon'
    
    context = {'details' : details,
               'rType' : rType,
               'playerName' : playerName,
               'title': 'GeekFest Geeks',
               'state':newstate,
               'stateinfo': zip(mainmenu.menu,mainmenu.page,mainmenu.state),
               }
    return HttpResponse(template.render(context, request))

def about(request):
    mainmenu = StateInfo()
    mainmenu.set('About')
    template = loader.get_template('about.html')
    context = {'title': 'About GeekFest', 'stateinfo': zip(mainmenu.menu,mainmenu.page,mainmenu.state), }
    return HttpResponse(template.render(context, request))


def buys(request):
    buycount = Buy.objects.all().prefetch_related('geek').values('item__name', 'geek__handle').annotate(num_buys=Count('buy_id')).order_by('-num_buys')
    template = loader.get_template('buys.html')
    mainmenu = StateInfo()
    mainmenu.set('About')
    context = {'buys': buycount, 'title': 'Buys', 'stateinfo': zip(mainmenu.menu,mainmenu.page,mainmenu.state), }
    return HttpResponse(template.render(context, request))







######################################
# .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------. 
#| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
#| |    ______    | || |  _________   | || |    _____     | || |     ____     | || |    _____     | || |    _____     | |
#| |  .' ___  |   | || | |_   ___  |  | || |   / ___ `.   | || |   .'    '.   | || |   / ___ `.   | || |   / ___ `.   | |
#| | / .'   \_|   | || |   | |_  \_|  | || |  |_/___) |   | || |  |  .--.  |  | || |  |_/___) |   | || |  |_/___) |   | |
#| | | |    ____  | || |   |  _|      | || |   .'____.'   | || |  | |    | |  | || |   .'____.'   | || |   .'____.'   | |
#| | \ `.___]  _| | || |  _| |_       | || |  / /____     | || |  |  `--'  |  | || |  / /____     | || |  / /____     | |
#| |  `._____.'   | || | |_____|      | || |  |_______|   | || |   '.____.'   | || |  |_______|   | || |  |_______|   | |
#| |              | || |              | || |              | || |              | || |              | || |              | |
#| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
# '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 
#######################################

def event(request):
    ##logic to get event awards and stuff
    template = loader.get_template('gf2023awards.html')
    mainmenu = StateInfo()
    mainmenu.set('Event')
    context = {'title': 'GF 2023', 'stateinfo': zip(mainmenu.menu,mainmenu.page,mainmenu.state), }
    return HttpResponse(template.render(context, request))
