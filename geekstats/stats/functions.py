#from django.db import connection
import stats.query as qry
import collections
#import query as qry
#import numpy as np
from dateutil.relativedelta import relativedelta
from datetime import date, datetime
data = []
import sys

class playerspecs:
    def __init__(self, record, state):
        self.id = record[0]
        self.kills = record[2]
        self.deaths = record[3]
        if record[3] == 0:
            self.kdr = 'n/a'
        else:
            self.kdr = round(record[2]/record[3],2)
        self.item = record[10]
        state.clause = state.compare +' = "'+record[10]+'" '
        self.details = qry.get_query('detaildetails',state)
    
class player:
    def __init__(self, record):
        self.id = record[0]
        self.handle = record[1]
        self.kills = record[2]
        self.deaths = record[3]
        if record[3] == 0:
            self.kdr = 'n/a'
        else:
            self.kdr = round(record[2]/record[3],2)
        self.tier = record[4]
        if record[5] == 1:
            self.gen = 'GenX'
        elif record[5] == 2:
            self.gen = 'GenY'
        elif record[5] == 3:
            self.gen = 'GenZ'
        self.firstname = record[6]
        self.lastname = record[7]
        self.membersince = record[8]
        self.years = (relativedelta(date.today(), self.membersince).years)+round((relativedelta(date.today(), self.membersince).months)/12,2)
        self.location = record[9]
        self.team = ''
        self.kdr_avg = record[10]
        self.maps_played = record[11]
        if self.kdr == 'n/a':
            self.kdr_v_avg = 'n/a'
        else:
            self.kdr_v_avg = self.kdr - self.kdr_avg
        self.weapons = []
        self.maps = []
        self.opponents = []

        def __str__(self):
            return self.handle
class games:
    def __init__(self, data):
        self.date = data[6]
        self.gamedata = []

    def addgame(self, data):
        self.gamedata.append(data)

    def __str__(self):
        return self.date        
    
class season:
    def __init__(self, title, data):
        self.name = title
        self.team1 = data[0][1]
        self.team1avg = 0
        self.team1wins = 0
        self.team1rdwins = 0
        self.team2 = data[0][3]
        self.team2avg = 0
        self.team2wins = 0
        self.team2rdwins = 0
        self.rounds = []
    def addGame(self, data):
        firstdate = data[0][6]
        counter = 0
        for num, i in enumerate(data):
##            print(counter)
##            print('Does '+str(i[6])+' = '+str(firstdate)+'?')
            if i[6] == firstdate:
##                print('YES!')
                if num == 0:
                    self.rounds.append(games(i))
                    self.rounds[counter].addgame(i)
                else:
                    self.rounds[counter].addgame(i)
            else:
##                print('NO!')
                counter+=1
                firstdate = i[6]
                self.rounds.append(games(i))
                self.rounds[counter].addgame(i)
    def calcAvg(self, players):
        team1count = team2count = team1total = team2total = 0
        for i in players:
            if i.team == self.team1:
#                print('team 1: '+str(team1total)+' + '+str(i.kdr)+' = '+str(team1total+i.kdr)+' count is: '+str(team1count)+' for player '+i.handle)
                team1total += i.kdr
                team1count += 1
            elif i.team == self.team2:
#                print('team 2: '+str(team2total)+' + '+str(i.kdr)+' = '+str(team2total+i.kdr)+' count is: '+str(team2count)+' for player '+i.handle)
                team2total += i.kdr
                team2count += 1
        if team1count == 0:
            self.team1avg = 'n/a'
            self.team2avg = 'n/a'
        else: 
            self.team1avg = round(team1total / team1count,2)
            self.team2avg = round(team2total / team2count,2)

    def calcWins(self):        
        for i in self.rounds:
            cTeam1rdwins = cTeam2rdwins = 0
            cTeam1wins = cTeam2wins = 0
            print(i.date)
            for j in i.gamedata:
                try:                    
                    cTeam1rdwins += j[2]
                    cTeam2rdwins += j[4]
                    if j[2] > j[4]:
                        cTeam1wins += 1
                    else:
                        cTeam2wins += 1
                except:
                    cTeam1rdwins += 0
                    cTeam2rdwins += 0
                    
            self.team1rdwins += cTeam1rdwins
            self.team2rdwins += cTeam2rdwins
            print('at this point, team 1 has: '+str(cTeam1rdwins))
            if cTeam1wins > cTeam2wins:
                self.team1wins += 1
            elif cTeam1wins < cTeam2wins:
                self.team2wins += 1
            else:
                if cTeam1rdwins < cTeam2rdwins:
                    self.team2wins += 1
                elif cTeam1rdwins > cTeam2rdwins:
                    self.team1wins += 1

                    

            
#        print('team 1 won '+str(self.team1wins)+' and '+str(self.team1rdwins)+' rounds')

    def __str__(self):
        return self.name

class detail_stats:
    def __init__(self, record, data):
        self.detail = record
        self.playerscores = []
        for i in data:
            self.playerscores.append(player(i))

    def __str__(self):
        return self.detail            

class playerGraph:
    def __init__(self, details):
        self.id = details[0][0]
        self.handle = details[0][1]
        self.deaths = []
        self.kills = []
        self.date = []
        self.kdr = []
        for i in details:
            self.deaths.append(str(i[2]))
            self.kills.append(str(i[3]))
            self.date.append(str(i[4])[-5:])
            if i[2]>0:
                self.kdr.append(str(round(i[3]/i[2],2)))
            else:
                self.kdr.append('0')

    def __str__(self):
        return self.handle
##class state:
##    def __init__(self):
##        self.start_date = '2019-02-09'
##        self.end_date = '2019-02-09'
##        self.compare = ''
##        self.operator = ''
##        self.value = 0
##        self.season = ''

class awards:
    def __init__(self, award, players, desc, group, image, description, color, groupid):
        self.award = award
        self.winners = players
        self.description = desc
        self.group = group
        self.image = image
        self.color = color
        self.longdesc = description
        self.groupid = groupid

## Sets colors for values on KDR
def set_color(score):
    style = ''
    if score == 'ND':
        style+=('#000000;')
    elif score < .25:
        style+=('#a50026;')
    elif score < .5:
        style+=('#d3322b;')
    elif score < .75:
        style+=('#f16d43;')
    elif score < 1:
        style+=('#fcab63;')
    elif score < 1.25:
        style+=('#fedc8c;')
    elif score < 1.5:
        style+=('#f9f7ae;')
    elif score < 1.75:
        style+=('#d7ee8e;')
    elif score < 2:
        style+=('#a4d86f;')
    elif score < 2.5:
        style+=('#64bc61;')
    elif score < 3:
        style+=('#23964f;')
    else:
        style+=('#0364429;')
    style+=';"'
    return style

## Gets stats data with kdr (tiers, standings, etc...)
def get_stats_data(state):
    data=[]
    results = qry.get_query('frags',state)
    for i in results:
        data.append(player(i))
    return data

## Gets stats data with just kills or deaths but includes maps and/or weapons
def get_details(state):
    data=[]
    details = (qry.get_query('values',state))
    for i in details:
        state.value = i[0]
        data.append(detail_stats(i[0],qry.get_query('details',state)))
    return data

## Uses award list to calculate awards
def get_awards(state):
    data = []
    print(state.value)
    if state.value == 0 or state.value =='' or state.value == '0':
        state.clause = 'select distinct class, color from gf_awards;'
        award_names = qry.get_query('simple',state)
    elif state.value == 'event':
        award_names = [['gfxx']]
    else:
        state.clause = 'select distinct class, color from gf_awards where class = "'+state.value+'";'
        award_names = qry.get_query('simple',state)

    for a in award_names:
        state.compare = a[0]
        award_data = qry.get_query('val_awards',state)
        for i in award_data:
            state.compare = i[3]
            winners = awards(i[1],(qry.get_query(i[2], state)), i[4], i[5], i[6], i[7], i[8])
            data.append(winners)
    state.clause = 'select distinct class, color from gf_awards;'
    award_names = qry.get_query('simple',state)
    return award_names, data

## Gets the unique list of values for dates, weapons, maps, players, etc...
def get_unique_values(state):
    data = []
    details = (qry.get_query('values',state))

## Gets the list of seasons
def get_seasons(state):
    data = []
    data = qry.get_query('seasons',state)
    return data

## Gets the necessary team data
def get_team_seasons(state, request):
    data = []
    data = qry.get_query('seasons',state)
    if request.method == 'POST':
        for i in data:
            if i[0] == request.POST['seasonList']:
                print('we are processing')
                request.session['start_date'] = str(i[1])
                request.session['end_date'] = str(i[2])
                request.session['season'] = i[0]
    else:
        request.session['start_date'] = str(data[0][1])
        request.session['end_date'] = str(data[0][2])
        request.session['season'] = data[0][0]
        
    return data

def get_team_data(state):
    print(state.start_date, state.end_date, state.season)
    data = qry.get_query('games',state)
    SeasonData = season(state.season, data)
    SeasonData.addGame(data)
            
    data_team_members = qry.get_query('teams',state)
    print(data_team_members)
    data_players = get_stats_data(state)
    for i in data_team_members:
        for j in data_players:
            if (i[3].upper()).strip() == (j.handle.upper()).strip():
                j.team = i[0]
    if not data_players:
        print('no games have been played')
    else:        
        SeasonData.calcWins()
        SeasonData.calcAvg(data_players)

    return SeasonData, data_players

def get_player_details(state):
    state.compare = 'playerId'
    playerinfo = player(qry.get_query('frags',state)[0])
    state.compare = 'map'
    maps = qry.get_query('playerdetails',state)
    for i in maps:
        playerinfo.maps.append(playerspecs(i, state))
    state.compare = 'weapon'
    weapons = qry.get_query('playerdetails',state)
    for i in weapons:
        if i[2] > 0:
            playerinfo.weapons.append(playerspecs(i, state))

    state.compare = 'weapon'
    kills = qry.get_query('playerperf',state)
    for i in kills:
        playerinfo.opponents.append(playerspecs(i, state))
    for i in playerinfo.opponents:
        print(i.item)
        for j in i.details:
            print('DETAILS: '+str(j))

    ## Build mouseover functionality for stat details
    return playerinfo

def get_pdetails(state, request):
    if request.session['opponentid'] != '':
        state.compare = '(g1.handle = "'+str(request.session['opponentid'])+'" OR g2.handle = "'+str(request.session['opponentid']+'")')
    elif request.session['weaponid'] != '':
        state.compare = 'weapon = "'+str(request.session['weaponid'])+'"'
    elif request.session['mapid'] != '':
        state.compare = 'map = "'+str(request.session['mapid'])+'"'
    state.value = request.session['playerid']
    data = qry.get_query('pdetails',state)
    return data

def get_perf_data(state):
    data = qry.get_query('perf_data',state)
    graph_data = playerGraph(data)
    return graph_data

def unique_dates(datelist):
    xDates = []
    for i in datelist:
        if xDates.count(i['match_date'].strftime("%m-%d-%Y")) == 0:
            xDates.append(i['match_date'].strftime("%m-%d-%Y"))
    return xDates 
        
    
##    df = qry.get_df()
##    dates = df.eDate.unique()                                       #finds unique dates for header data
##    dates.sort()                                                    #ensures dates are in sequential order
##    playcounts = df.handle.value_counts()                           #counts the number of players for the data table
##    geek_shortlist = df[df.handle.isin(playcounts.index[playcounts.gt(1)])] #eliminates any players who have only played 1 time
##    geeks = geek_shortlist.handle.unique()                          #sets up the geek names data set
##    output = []
##    row = ['<th style="background:black; font-size:10px; color:white;">handle</th>']
##    for i in dates:                                               #Build the date headers
##        row.append('<th style="background:black; font-size:10px; color:white;">'+str(i)+'</th>')
##    output.append(row)
##
##    for g in geeks:                                               #Build the data for each player
##        row = []
##        row.append('<td style="font-size:10px;">'+g+'</td>')
##        KTDs = df.loc[df['handle']==g]                              #Stage the data for the player
##        x=0                                                         #Counter for dates to line up columns when data is missing for a date
##        for i,j in KTDs.iterrows():
##            while dates[x] != j[3]:                                 #Iterates the date counter and fills in blanks when data value does not match date header
##                
##                row.append('<TD style="background:black; font-size:10px;">ND</TD>')                                    #Displays "ND" if the current value does not line up with the header date
##                x+=1                                                #Iterates the counter to move to the next date
##            kdr = round((j[1]/j[2]),2)
##            bgd = set_color(kdr)
##            row.append('<TD style=" font-size:10px; text-align:center; background:'+bgd+'">'+str(kdr)+'</td>')                        #displays the data after / when it alignes to date header
##            x+=1                                                    #Iterates the counter to move to the next date after match to setup next data item
##        while x < len(dates):                                       #If a player's data ends before all dates have been iterated, this fills in the remaining slots
##            row.append('<TD style="background:black; font-size:10px;">ND</TD>')                                    
##            x+=1
##        output.append(row)
##
##    return output

##newstate = state()
##x = get_team_seasons(newstate)
##newstate.season = x[0][0]
##newstate.compare = x[0][0]
##newstate.start_date = x[0][1]
##newstate.end_date = x[0][2]
##y,z = get_team_data(newstate)

##players=[]
##
##players = get_stats_data(newstate)
##for i in players:
##    print (i.handle, str(i.kdr))
##
##newstate.compare = 'weapon'
##weapons = get_details(newstate)
##newstate.compare = 'code'
##newstate.operator = 'like'
##newstate.value = 'kill_streak%'
##killstreak = get_awards(newstate)


