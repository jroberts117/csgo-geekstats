from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .geekmodels import Buy, TeamWins, TiersData, Frag, MatchRound, Death, SeasonMatch
from .geekclasses import season
import stats.functions as func
import operator, sys
from django.db.models import Count, Sum, Avg
import datetime
from datetime import date, timedelta

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
        self.menu = ['Event','Awards','Tiers','Teams','Maps','Weapons','Geeks']
        self.state = ['','','','','','','']

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
    def setsession(self,start,end,compare,value,page, selector):
        self.start_date = start
        self.end_date = end
        self.compare = compare
        self.value = value
        self.page = page
        self.selector = selector

#################  Global Variables ##########################
mainmenu = StateInfo()
newstate = state()
#################  Functions ##########################

def index(request):
##    geeks = Geeks.objects.order_by('handle')
    template = loader.get_template('index.html')
    context = {'title': 'GeekFest Stats'}
    return HttpResponse(template.render(context, request))

def awards(request):
    mainmenu.set('Awards')
    template = loader.get_template('awards.html')
    newstate.setsession(request.session['start_date'],request.session['end_date'],'',0,'Awards', request.session['selector'])
    try:
        newstate.value=request.GET['aid']
        request.session['aid'] = newstate.value
    except:
        try:
            newstate.value = request.session['aid']
        except:
            newstate.value = 0
            
    award_types, awards = func.get_awards(newstate)
    context = {'awards': awards,
               'types' : award_types,
               'title': 'GeekFest Awards',
               'stateinfo': zip(mainmenu.menu,mainmenu.state),
               'eventdates':request.session['eventdates'],
               'state':newstate,
               }
    return HttpResponse(template.render(context, request))

def teams(request):
    ### INITIALIZE THE PAGE AND SESSION DATA
    mainmenu.set('Teams')
    template = loader.get_template('teams.html')
    seasons = func.get_team_seasons(newstate,request)
    newstate.season = request.session['season']
    newstate.setsession(request.session['start_date'],request.session['end_date'],'',0,'Teams', request.session['selector'])

    ### BUILD THE TEAMS DATA
    seasonData = TeamWins.objects.values().filter(match_date__gte=request.session['start_date'], match_date__lte=request.session['end_date']).order_by('-match_date')
    teamInfo = season(newstate.season)
    teamInfo.setTeams(TeamWins.objects.values('team_name').filter(match_date__gte=request.session['start_date'], match_date__lte=request.session['end_date']).distinct())
    dates = TeamWins.objects.values('match_date').filter(match_date__gte=request.session['start_date'], match_date__lte=request.session['end_date']).distinct()
    for date in dates:
        teamInfo.addMatches(TeamWins.objects.values().filter(match_date=date['match_date']).order_by('map'))

    teamInfo.calcWins()
    
    games,players = func.get_team_data(newstate)
    context = {'seasons': seasons,
               'gfgames':teamInfo,
               'players': players,
               'games': games,
               'title': 'GeekFest Teams',
               'stateinfo': zip(mainmenu.menu,mainmenu.state),
               'eventdates':request.session['eventdates'],
               'state':newstate,
               }
    return HttpResponse(template.render(context, request))

def tiers(request):
    mainmenu.set('Tiers')
    context={}
    template = 'tiers.html'
    newstate.setsession(request.session['start_date'],request.session['end_date'],'',0,'Tiers', request.session['selector'])
    context['title'] = 'GeekFest Tiers'
    context['stateinfo'] = zip(mainmenu.menu,mainmenu.state)
    context['eventdates'] = request.session['eventdates']
    context['state'] = newstate
    context['tier0'] = TiersData.objects.values('player')\
                       .filter(tier="Master", matchdate__gte=request.session['start_date'], matchdate__lte=request.session['end_date'])\
                       .order_by('-kdr__avg').annotate(Avg('kdr'))
    context['tier1'] = TiersData.objects.values('player').filter(tier="Gold", matchdate__gte=request.session['start_date'], matchdate__lte=request.session['end_date']).order_by('-kdr__avg').annotate(Avg('kdr')) 
    context['tier2'] = TiersData.objects.values('player').filter(tier="Silver", matchdate__gte=request.session['start_date'], matchdate__lte=request.session['end_date']).order_by('-kdr__avg').annotate(Avg('kdr'))
    context['tier3'] = TiersData.objects.values('player').filter(tier="Bronze", matchdate__gte=request.session['start_date'], matchdate__lte=request.session['end_date']).order_by('-kdr__avg').annotate(Avg('kdr'))
    context['players'] = TiersData.objects.values('player','tier').filter(matchdate__gte=request.session['start_date'], matchdate__lte=request.session['end_date']).order_by('-kdr__avg').annotate(Avg('kdr'),Sum('kills'),Sum('deaths'),Sum('assists'),Avg('akdr'))
    avgkdr = TiersData.objects.values('player').filter(matchdate__gte=newstate.days180ago, matchdate__lte=newstate.today).annotate(Avg('kdr'))
    players = list(context['players'])
    for geek in players:
        for item in avgkdr:
            if geek['player'] == item['player']:
                geek['avgkdr'] = item['kdr__avg']
                geek['diffkdr'] = geek['kdr__avg'] - item['kdr__avg']
    context['players'] = players

    return render(request, template, context)

##### GEEKFEST XX: VIRTUAL CODE ######
def gfxx(request):
    mainmenu.set('Event')
    template = loader.get_template('gfxxv.html')
    newstate.setsession('2020-12-02','2020-12-02','',0,'Event', request.session['selector'])

    players = func.get_stats_data(newstate)
    players.sort(key=lambda players: players.kdr_v_avg, reverse=True)
    print(players[0])
    v_avg=[players[0],players[-1]]
    
    players.sort(key=lambda players: players.kdr, reverse=True)
     
    tier0 = [x for x in players if x.tier == 0]
    tier1 = [x for x in players if x.tier == 1]
    tier2 = [x for x in players if x.tier == 2]
    tier3 = [x for x in players if x.tier == 3]

    newstate.value = 'event'
    award_types, awards = func.get_awards(newstate)
    

    context = {'tier0':tier0, 'tier1': tier1, 'tier2': tier2, 'tier3':tier3, 'players':players, 'v_avg': v_avg,
               'awards': awards, 'types':award_types,
               'title': 'GeekFest Tiers',
               'stateinfo': zip(mainmenu.menu,mainmenu.state),
               'eventdates':request.session['eventdates'],
               'state':newstate,
               }
    return HttpResponse(template.render(context, request))

def maps(request):
    mainmenu.set('Maps')
    template = loader.get_template('maps.html')
    newstate.setsession(request.session['start_date'],request.session['end_date'],'',0,'Maps', request.session['selector'])
    newstate.compare = 'map'
    #TiersData.objects.values('player').filter(tier="Gold", matchdate__gte=request.session['start_date'], matchdate__lte=request.session['end_date']).order_by('-kdr__avg').annotate(Avg('kdr')) 
    endDate = datetime.datetime.strptime(request.session['end_date'], '%Y-%m-%d') + datetime.timedelta(days=1)
    rounds = MatchRound.objects.prefetch_related('match').filter(match__match_date__gte=request.session['start_date'], match__match_date__lte=endDate.strftime('%Y-%m-%d %H:%M:%S'))

    killData = Frag.objects.prefetch_related('geek').prefetch_related('round__match').filter(round__in=rounds, is_teamkill=False, geek__is_member=True).values('round__match__map', 'geek__handle', 'geek_id', 'round__match__match_date').annotate(num_frags=Count('frag_id')).order_by('round__match__match_date', '-num_frags')
    deathData = Death.objects.prefetch_related('geek').prefetch_related('round__match').filter(round__in=rounds, is_teamkill=False, geek__is_member=True).values('round__match__map', 'geek__handle', 'geek_id').annotate(num_deaths=Count('death_id')).order_by('round__match__map')

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


    context = {'title': 'GeekFest Maps', 
               'stateinfo': zip(mainmenu.menu,mainmenu.state),
               'eventdates':request.session['eventdates'],
               'state':newstate,
               'mapstats':mapGroupData.values
               }
    return HttpResponse(template.render(context, request))


def weapons(request):
    mainmenu.set('Weapons')
    template = loader.get_template('weapons.html')
    newstate.setsession(request.session['start_date'],request.session['end_date'],'',0,'Weapons', request.session['selector'])

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
               'eventdates':request.session['eventdates'],
               'state':newstate,
               'stateinfo': zip(mainmenu.menu,mainmenu.state), }
    return HttpResponse(template.render(context, request))

def geeks(request):
    mainmenu.set('Geeks')
    template = loader.get_template('geeks.html')
    newstate.setsession(request.session['start_date'],request.session['end_date'],'',0,'Geeks', request.session['selector'])

    geeks = func.get_stats_data(newstate)
    geeks.sort(key=lambda x: x.years, reverse=True)
    
    context = {'geeks': geeks,
               'title': 'GeekFest Geeks',
               'eventdates':request.session['eventdates'],
               'state':newstate,
               'stateinfo': zip(mainmenu.menu,mainmenu.state),
               }
    return HttpResponse(template.render(context, request))

def playerdetails(request):
    mainmenu.set('Geeks')
    template = loader.get_template('playerdetails.html')
    newstate.setsession(request.session['start_date'],request.session['end_date'],'',request.session['playerid'],'PlayerDetails', request.session['selector'])

    graph = func.get_perf_data(newstate)
    info = func.get_player_details(newstate)


    context = {'player': info,
               'graph': graph,
               'title': 'GeekFest Geeks',
               'eventdates':request.session['eventdates'],
               'state':newstate,
               'stateinfo': zip(mainmenu.menu,mainmenu.state),
               }
    return HttpResponse(template.render(context, request))

def details(request):
    mainmenu.set('Geeks')
    template = loader.get_template('details.html')
    newstate.setsession(request.session['start_date'],request.session['end_date'],'',request.session['playerid'],'PlayerDetails', request.session['selector'])
    detailinfo = [request.session['playerid'],request.session['opponentid'],request.session['mapid'],request.session['weaponid']]

    details = func.get_pdetails(newstate, request)
    context = {'details' : details,
               'detailinfo' : detailinfo,
               'title': 'GeekFest Geeks',
               'eventdates':request.session['eventdates'],
               'state':newstate,
               'stateinfo': zip(mainmenu.menu,mainmenu.state),
               }
    return HttpResponse(template.render(context, request))

def about(request):
    #geeks = Geeks.objects.order_by('handle')
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



