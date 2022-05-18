from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse
from django.template import loader
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from .geekmodels import Buy, Geek, TeamWins, TiersData, Frag, MatchRound, Death, SeasonMatch, GeekInfo, FragDetails, GeekfestMatchAward, AwardCategory, Season, GeekAuthUser
from .geekclasses import season, player
import stats.functions as func
from .forms import CustomUserCreationForm
import logging
import operator, sys
from django.db.models import Count, Sum, Avg, Min, Max, Q
import datetime
import uuid
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
        self.menu = ['Awards','Tiers','Teams','Maps','Weapons','Geeks']
##        self.menu = ['Tiers','Teams','Maps','Weapons','Geeks']
        self.state = ['','','','','','','', '']

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

    ### BUILD THE SEASON PICKLIST AND LOAD THE SESSION DATA BASED ON INPUT
#     seasons = Season.objects.values().order_by('-start_date')
#     if request.POST.get('seasonList',False):
#         curr_season = Season.objects.values().filter(name=request.POST['seasonList'])
#         request.session['start_date'] = curr_season[0]['start_date'].strftime('%Y-%m-%d')
#         request.session['end_date'] = curr_season[0]['end_date'].strftime('%Y-%m-%d')
#         request.session['season'] = curr_season[0]['name']
#     else:
#         request.session['start_date'] = seasons[0]['start_date'].strftime('%Y-%m-%d')
#         request.session['end_date'] = seasons[0]['end_date'].strftime('%Y-%m-%d')
#         request.session['season'] = seasons[0]['name']
# ##    seasons = func.get_team_seasons(newstate,request)
    if request.session['datetype'] != 'season':
        curr_season = Season.objects.values().order_by('-start_date')
        request.session['start_date'] = curr_season[0]['start_date'].strftime('%Y-%m-%d')
        request.session['end_date'] = curr_season[0]['end_date'].strftime('%Y-%m-%d')
        request.session['datetype'] = 'season'

    newstate.setsession(request.session['start_date'],request.session['end_date'],'',0,'Teams', request.session['selector'],request.session['datetype'])

    ### BUILD THE TEAMS DATA
    seasonData = TeamWins.objects.values().filter(match_date__gte=request.session['start_date'], match_date__lte=request.session['end_date']).order_by('-match_date')
    teamInfo = season(newstate.season)
    if seasonData:
        teamInfo.setTeams(TeamWins.objects.values('team_name').filter(match_date__gte=request.session['start_date'], match_date__lte=request.session['end_date']).distinct())
        dates = TeamWins.objects.values('match_date').filter(match_date__gte=request.session['start_date'], match_date__lte=request.session['end_date']).distinct()
        for date in dates:
            teamInfo.addMatches(TeamWins.objects.values().filter(match_date=date['match_date']).order_by('map'))

        teamInfo.calcWins()
    
#    games,players = func.get_team_data(newstate)
    context = {'gfgames':teamInfo,
#               'players': players,
#               'games': games,
               'title': 'GeekFest Teams',
               'stateinfo': zip(mainmenu.menu,mainmenu.state),
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
    context['stateinfo'] = zip(mainmenu.menu,mainmenu.state)
    context['state'] = newstate
    context['players'] = TiersData.objects.values('geekid','player','tier','tier_id','year_kdr').filter(matchdate__gte=request.session['start_date'], matchdate__lte=request.session['end_date']).order_by('-kdr__avg').annotate(Avg('kdr'),Sum('kills'),Sum('deaths'),Sum('assists'),Avg('akdr'))
    context['tier0'] = list(filter(lambda tiers: tiers['tier_id'] == 1, list(context['players'])))
    context['tier1'] = list(filter(lambda tiers: tiers['tier_id'] == 2, list(context['players'])))
    context['tier2'] = list(filter(lambda tiers: tiers['tier_id'] == 3, list(context['players'])))
    context['tier3'] = list(filter(lambda tiers: tiers['tier_id'] == 4, list(context['players'])))

    for geek in context['players']:
        try:
            geek['diffkdr'] = geek['kdr__avg'] - geek['year_kdr']
        except:
            geek['diffkdr'] = 'n/a'


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
    # map_list = []
    # for i in mapGroupData:
    #     map_list.append(i)
    # playData = (MatchRound.objects.values('win_side','match_id__map').filter(match__map__in=map_list)
    #             .annotate(num_plays=Count('round_id')).order_by('match_id__map','win_side'))
    
    # print(playData)
    # print(mapGroupData)
    # for i in mapGroupData:
    #     for j in playData:
    #         if i == j['match_id__map']:
                # if j['win_side'] == 'CT':
                #     i['CT'] = j['num_plays']
                # else:
                #     i['T'] = j['num_plays']

                # print(j['match_id__map'], j['win_side'], str(j['num_plays'], i.values))

    context = {'title': 'GeekFest Maps', 
               'stateinfo': zip(mainmenu.menu,mainmenu.state),
               'state':newstate,
               'mapstats':mapGroupData.values,
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
               'stateinfo': zip(mainmenu.menu,mainmenu.state), }
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
               'state':newstate,
               'stateinfo': zip(mainmenu.menu,mainmenu.state),
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

    ### SETUP VALIDATION LOGIC FOR REGISTERED PLAYERS
    geek = GeekAuthUser.objects.values('geek_id','handle','valid_sent_date','validated','username','first_name','email','member_since').filter(geek_id=pid) 
    lst = list(geek)
    if request.GET.get('claim'):
        claim = request.GET.get('claim')
        if claim == 'claim' or claim == 'resend':
            geek_code = uuid.uuid4()
            password = geek[0]['first_name']+geek[0]['member_since'].strftime('%m%Y')
            # httplink = 'http://192.168.0.156:8000/Geeks?code='+str(geek_code)
            httplink = 'http://cs.geekfestclan.com/Geeks?code='+str(geek_code)
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

        # lst = list(pdata.all())
        kdata = list(filter(lambda p: p['type'] == 'kill', list(pdata)))
        laplayer = list(filter(lambda p: p['type'] == 'assist', list(pdata)))
        lkplayer = list(filter(lambda w: str(w['id']) == pid, list(kdata)))
        lvplayer = list(filter(lambda w: str(w['victim_id']) == pid, list(kdata)))

        playerData.addWeapons('killer','weapon',listbuilder(lkplayer,'weapon'))
        playerData.addWeapons('victim','weapon',listbuilder(lvplayer,'weapon'))
        playerData.addMaps('killer','map',listbuilder(lkplayer,'map'))
        playerData.addMaps('victim','map',listbuilder(lvplayer,'map'))
        playerData.addMaps('assist','map',listbuilder(laplayer,'map'))
        playerData.addOpps('killer','victim',listbuilder(lkplayer,'victim'))
        playerData.addOpps('victim','killer',listbuilder(lvplayer,'killer'))

        playerData.calcStats()
    
    context = {'player': playerData,
               'geek': geek,
               'title': 'GeekFest Geeks',
               'state':newstate,
               'stateinfo': zip(mainmenu.menu,mainmenu.state),
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

    ### GET THE DETAILS REQUESTED FROM THE FRAGDETAILS VIEW
    if request.session['opponentid'] != '':
        pdetails = FragDetails.objects.values().filter(id=pid,victim=xOpp,match_date__gte=request.session['start_date'], match_date__lte=request.session['end_date']).order_by('match_datetime')
        details = pdetails.union(FragDetails.objects.values().filter(victim_id=pid,killer=xOpp,match_date__gte=request.session['start_date'], match_date__lte=request.session['end_date']).order_by('match_datetime'),all=True).order_by('match_datetime')
    elif xMap != '':
        pdetails = FragDetails.objects.values().filter(id=pid,map=xMap,match_date__gte=request.session['start_date'], match_date__lte=request.session['end_date']).order_by('match_datetime')
        details = pdetails.union(FragDetails.objects.values().filter(victim_id=pid,map=xMap,match_date__gte=request.session['start_date'], match_date__lte=request.session['end_date']),all=True).order_by('match_datetime')
    elif xWeapon != '':
        pdetails = FragDetails.objects.values().filter(id=pid,weapon=xWeapon,match_date__gte=request.session['start_date'], match_date__lte=request.session['end_date']).order_by('match_datetime')
        details = pdetails.union(FragDetails.objects.values().filter(victim_id=pid,weapon=xWeapon,match_date__gte=request.session['start_date'], match_date__lte=request.session['end_date']),all=True).order_by('match_datetime')
    context = {'details' : details,
               'title': 'GeekFest Geeks',
               'state':newstate,
               'stateinfo': zip(mainmenu.menu,mainmenu.state),
               }
    return HttpResponse(template.render(context, request))

def about(request):
    mainmenu = StateInfo()
    mainmenu.set('About')
    template = loader.get_template('about.html')
    context = {'title': 'About GeekFest', 'stateinfo': zip(mainmenu.menu,mainmenu.state), }
    return HttpResponse(template.render(context, request))


def buys(request):
    buycount = Buy.objects.all().prefetch_related('geek').values('item__name', 'geek__handle').annotate(num_buys=Count('buy_id')).order_by('-num_buys')
    template = loader.get_template('buys.html')
    mainmenu = StateInfo()
    mainmenu.set('About')
    context = {'buys': buycount, 'title': 'Buys', 'stateinfo': zip(mainmenu.menu,mainmenu.state), }
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
    template = loader.get_template('event.html')
    mainmenu = StateInfo()
    mainmenu.set('Event')
    context = {'title': 'GF 2022', 'stateinfo': zip(mainmenu.menu,mainmenu.state), }
    return HttpResponse(template.render(context, request))
