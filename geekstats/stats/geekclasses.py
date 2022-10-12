# This module contains custom classes for use in geekstats
#  * These classes need to be manually included in other programs to be referenced
#  * Custom class objects provide a logical structure to store data for
#  * display when leveraging data models becomes too cumbersome

from .geekmodels import Geek, TiersData, TeamGeek
from django.db import models
from django.db.models import Count, Sum, Avg, Min, Max, Q, F, ExpressionWrapper, Value


########################################################################
### ROUND
###     This class contains the data for a round which includes the map
###     and scores for the round
########################################################################
class gfRound:
    def __init__(self, data):
        self.map = data
        self.score = [0,0]

    def __str__(self):
        return self.map        

########################################################################
### MATCH
###     This class contains the data for match on a given date
########################################################################
class gfMatch:
    def __init__(self, data):
        self.date = data            # date of match
        self.team1rdwins = 0        # counter for rounds wins within match
        self.team2rdwins = 0
        self.team1wins = 0
        self.team2wins = 0
        self.round = []             # list of round class

    def addgame(self, data):
        self.gamedata.append(data)

    def __str__(self):
        return self.date
    

########################################################################
### SEASON
###     This class contains the high level data for for a season to be
###     displayed on the teams page
########################################################################
class season:
    def __init__(self, seasondata):
        self.name = seasondata['name']
        self.description = seasondata['description']
        self.master_winner = seasondata['master_win__handle']
        self.gold_winner = seasondata['gold_win__handle']
        self.silver_winner = seasondata['silver_win__handle']
        self.bronze_winner = seasondata['bronze_win__handle']
        self.team1 = ''
        self.team1avg = 0
        self.team1wins = 0
        self.team1matchwins = 0
        self.team1rdwins = 0
        self.team2 = ''
        self.team2avg = 0
        self.team2wins = 0
        self.team2matchwins = 0
        self.team2rdwins = 0
        self.match = []
        self.team1players = []
        self.team2players = []
        self.team1startkdr = 0
        self.team1seasonkdr = 0
        self.team2startkdr = 0
        self.team2seasonkdr = 0

    def setTeams(self, data):
        print(data[0]['team_name'])
        self.team1 = data[0]['team_name']
        self.team2 = data[1]['team_name']
##        print(self.team1, self.team2)
        
    def addMatches(self, data):
        curr_match = gfMatch(data[0]['match_date'])
        curr_map = 'none'
        for row in data:
            if row['map'] != curr_map:
                if curr_map != 'none':
                    curr_match.round.append(curr_round)
                curr_round = gfRound(row['map'])
            if row['team_name'] == self.team1:
                curr_round.score[0] = int(row['wins'])
            else:
                curr_round.score[1] = int(row['wins'])
            curr_map = row['map']
        curr_match.round.append(curr_round)
        self.match.append(curr_match)

    def addPlayers(self, data, team):
        for i in data:
            if team == 1:
                self.team1players.append(player([i]))
                self.team1startkdr += i['alltime_kdr']
                self.team1seasonkdr += i['kdr__avg']
            else:
                self.team2players.append(player([i]))
                self.team2startkdr += i['alltime_kdr']
                self.team2seasonkdr += round(i['kdr__avg'],2)

    def set_player_list(self, request, team, teamnbr):
        team_data = TeamGeek.objects.values('geek','team','tier').filter(team__name=team)
        temp_list = []
        for i in team_data:
            temp_list.append(i['geek'])
        tempPlayers = TiersData.objects.values('geekid','player','tier','tier_id','year_kdr','alltime_kdr').filter(geekid__in=temp_list, matchdate__gte=request.session['start_date'], matchdate__lte=request.session['end_date']).order_by('-kdr__avg').annotate(Avg('kdr'),Sum('kills'),Sum('deaths'),Sum('assists'),Avg('akdr'))
        temp_listNoScore = []
        for i in temp_list:
            found=0
            for j in tempPlayers:
                if i == j['geekid']:
                    found=1
                    break
            if not found:
                temp_listNoScore.append(i)

        tempGeeks = Geek.objects.values('tier','year_kdr','alltime_kdr').filter(geek_id__in=temp_listNoScore).annotate(player=F('handle'), geekid=F('geek_id'), 
                                        kills=Value(0, output_field=models.IntegerField()), kdr__avg=Value(0, output_field=models.IntegerField()), kills__sum=Value(0, output_field=models.IntegerField()),
                                        deaths__sum=Value(0, output_field=models.IntegerField()), assists__sum=Value(0, output_field=models.IntegerField()), akdr__avg=Value(0, output_field=models.IntegerField()))

        self.addPlayers(tempPlayers,teamnbr)
        self.addPlayers(tempGeeks,teamnbr)

    def calcWins(self):
        for match in self.match:
##            print(match.date)
            for round in match.round:
                self.team1rdwins += round.score[0]
                match.team1rdwins += round.score[0]
                self.team2rdwins += round.score[1]
                match.team2rdwins += round.score[1]
                if round.score[0] > round.score[1]:
                    self.team1matchwins += 1
                    match.team1wins += 1
                else:
                    self.team2matchwins += 1
                    match.team2wins += 1
            if match.team1wins > match.team2wins:
                self.team1wins += 1
            elif match.team1wins < match.team2wins:
                self.team2wins += 1
            else:
                if match.team1rdwins > match.team2rdwins:
                    self.team1wins += 1
                elif match.team1rdwins < match.team2rdwins:
                    self.team2wins += 1
##            print('At the end of match '+str(match.date))
##            print('Team 1 has '+str(match.team1rdwins)+' and Team 2 has '+str(match.team2rdwins))
##            print('Team 1 has '+str(self.team1wins)+' total wins, '+str(self.team1matchwins)+' match wins and '+str(self.team1rdwins)+' round wins')
##            print('Team 2 has '+str(self.team2wins)+' total wins, '+str(self.team2matchwins)+' match wins and '+str(self.team2rdwins)+' round wins')

    def __str__(self):
        return self.name

########################################################################
### ITEM
###     This class contains the data for a weapon, maps or opponents
###     This class is normally associated with the player object
########################################################################
class item:
    def __init__(self, data, mType, field):
        try:
            self.item = data[field]
            if mType == 'killer':
                self.kills = data['id__count']
                self.deaths = 0
                self.assists = 0
            elif mType == 'victim':
                self.kills = 0
                self.deaths = data['id__count']
                self.assists = 0
            elif mType == 'assist':
                self.kills = 0
                self.deaths = 0
                self.assists = data['id__count']
        except:
            self.item = 'No data'
        self.buys = 0
        self.kdr = 0.00
        self.kpb = 0.00

    def calcTotals(self):
        if self.deaths > 0:
            self.akdr = round((self.kills + (self.assists*.25)) / self.deaths,2)
            self.kdr = round(self.kills / self.deaths,2)
        else:
            self.akdr = 9.99
            self.kdr = 9.99
        
########################################################################
### PLAYER
###     This class contains the high level data for a player
###     It contains subclasses for opponent, map and weapon data
########################################################################
class player:
    def __init__(self, data):
        try:
            lst = list(data)                                                    # Cache data to avoid running the query multiple times
            self.id = data[0]['geekid']
            self.name = data[0]['player']
            self.kills = data[0]['kills__sum']
            self.deaths = data[0]['deaths__sum']
            self.assists = data[0]['assists__sum']
            self.KDR = round(data[0]['kdr__avg'],2)
            self.aKDR = round(data[0]['akdr__avg'],2)
            self.diff_alltime_kdr = round(self.KDR - data[0]['alltime_kdr'],2)
            self.alltime_kdr = data[0]['alltime_kdr']

        except:
            self.name = 'No data'
        
        self.avgKDR = 0.0
        self.diffAvg = 0.0
        self.topVictim = ''
        self.nemesis = ''
        self.topWeapon = ''
        self.lowWeapon = ''
        self.topMap = ''
        self.lowMap = ''
        self.topOpponent = ''
        self.lowOpponent = ''
        self.weapons = []
        self.opponents = []
        self.maps = []
        self.avatar = ''

    def addWeapons(self,mType,field,data):
        if mType == 'killer':
            for row in data:
                self.weapons.append(item(row,mType,field))
        elif mType == 'victim':
            for row in data:
                exists = False
                for line in self.weapons:
                    if line.item == row[field]:
                        line.deaths = row['id__count']
                        exists = True
                if not exists:   
                    self.weapons.append(item(row,mType,field))

    def addMaps(self,mType,field,data):
        if mType == 'killer':
            for row in data:
                self.maps.append(item(row,mType,field))
        elif mType == 'victim':
            for row in data:
                exists = False
                for line in self.maps:
                    if line.item == row[field]:
                        line.deaths = row['id__count']
                        exists = True
                if not exists:   
                    self.maps.append(item(row,mType,field))
        elif mType == 'assist':
            for row in data:
                exists = False
                for line in self.maps:
                    if line.item == row[field]:
                        line.assists = row['id__count']
                        exists = True
                if not exists:   
                    self.maps.append(item(row,mType,field))
                    
    def addOpps(self,mType,field,data):
        if mType == 'killer':
            self.topVictim = data[0][field]
            for row in data:
                self.opponents.append(item(row,mType,field))
        elif mType == 'victim':
            self.nemesis = data[0][field]
            for row in data:
                exists = False
                for line in self.opponents:
                    if line.item == row[field]:
                        line.deaths = row['id__count']
                        exists = True
                if not exists:   
                    self.opponents.append(item(row,mType,field))

    def calcStats(self):
        for row in self.maps:
            row.calcTotals()
        for row in self.weapons:
            row.calcTotals()
        for row in self.opponents:
            row.calcTotals()
##        self.opponents.sort(key=lambda x:x.kdr, reverse=True)
        self.maps.sort(key=lambda x:x.kdr, reverse=True)
            
        mapTotKill = sum(row.kills for row in self.maps)
        mapTotDeath = sum(row.deaths for row in self.maps)

########################################################################
### MAP Details
###     This class contains the detail level data for a map
########################################################################
class map_detail:
    def __init__(self, data):
        self.id = 0
        name = 'none'
        count = 0

########################################################################
### MAP
###     This class contains the high level data for a map
###     It contains subclasses for players and weapons used on it
########################################################################
class map_summary:
    def __init__(self, data):
        # print(data)
        self.id = data['idmap']
        self.name = data['map']
        self.description = data['description']
        self.type = data['type']
        self.theme = data['theme']
        self.rating = data['votescore']
        if data['metascore']:
            self.metascore = data['metascore']
            self.votes = data['votes']
        else:
            self.metascore = 'NR'
            self.votes = 0
        if data['ct_wins'] :
            self.t_wins = data['t_wins']
            self.ct_wins = data['ct_wins']
            self.balance = round((self.ct_wins / (self.ct_wins + self.t_wins))*100,1)
        else:
            self.t_wins = 0.00
            self.ct_wins = 0.00
            self.balance = 0.00
        self.last_play = data['last_play']
        self.top_player = 'none'
        self.top_gun = 'none'
        self.kills = 0
        self.ninja = 0
        self.thumb = 'none'
        self.plays = data['plays']
        if data['s_plays']:
            self.s_plays = data['s_plays']
        else:
            self.s_plays = 0
        self.players = []
        self.weapons = []
        self.hero_image = data['hero_image']




            
   
        
        
