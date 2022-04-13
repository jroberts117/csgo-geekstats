# This module contains custom classes for use in geekstats
#  * These classes need to be manually included in other programs to be referenced
#  * Custom class objects provide a logical structure to store data for
#  * display when leveraging data models becomes too cumbersome

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
    def __init__(self, title):
        self.name = title
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

    def setTeams(self, data):
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
            self.id = data[0]['geekid']
            self.name = data[0]['player']
            self.kills = data[0]['kills__sum']
            self.deaths = data[0]['deaths__sum']
            self.assists = data[0]['assists__sum']
            self.KDR = round(data[0]['kdr__avg'],2)
            self.aKDR = round(data[0]['akdr__avg'],2)
            self.diff_alltime_kdr = round(self.KDR - data[0]['alltime_kdr'],2)

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
        
            
   
        
        
