import mysql.connector
import pymysql
#import pandas as pd
import sys
server = "cs.geekfestclan.com"
database = "geekfest"
username = "geekfest"
password = "g33k"
#cnx = mysql.connector.connect(user=username, password=password, host=server,database=database)

##########  Main KDR calculator with just players and dates        
def get_query(query, state):
    if query == 'frags':
        qry = """
        select tot.fplayerid, handle, sum(tot.kills) as kills, sum(tot.deaths) as deaths,
        t.tier, t.generation, t.firstname, t.lastname, t.membersince, t.location, t.kdr_year, t.maps_played
        from (
            SELECT killerId as fplayerid, 0 as deaths, count(*) as kills
            FROM geekfest.hlstats_events_frags a
            WHERE date(a.eventTime) >= '{0}' and date(a.eventTime) <= '{1}'
            group by killerId
            UNION
            Select victimId as fplayerid, count(*) as deaths, 0 as kills
            FROM geekfest.hlstats_events_frags a
            WHERE date(a.eventTime) >= '{0}' and date(a.eventTime) <= '{1}'
            group by victimId) tot
        join geekfest.geeks t on tot.fplayerid = t.playerid
        """
        if state.compare != '':
            qry+=' and {2} = "{3}" '
            qry+=' group by playerid order by kills desc;'
            newquery = qry.format(state.start_date, state.end_date, state.compare, state.value)
        else:
            qry+=' group by playerid order by kills desc;'
            newquery = qry.format(state.start_date, state.end_date)

##    elif query == 'allfrags':
##        qry = """
##        select uu.playerid, g.handle, sum(uu.kills) as kills, sum(uu.deaths) as deaths,
##        g.tier, g.generation, g.firstname, g.lastname, g.membersince, g.location
##        from (
##            select killerid as playerid, count(*) as kills, 0 as deaths
##            from hlstats_events_frags 
##            where date(a.eventTime) >= '{0}' and date(a.eventTime) <= '{1}'
##            group by killerid
##            union
##            select victimid as playerid, 0 as kills, count(*) as deaths
##            from hlstats_events_frags f
##            where date(a.eventTime) >= '{0}' and date(a.eventTime) <= '{1}'
##            group by victimid
##        ) uu
##        left join geeks g on uu.playerid = g.playerid
##        """
##        if state.compare != '':
##            qry+=' where {2} = "{3}" '
##            qry+=' group by uu.playerid order by kills desc;'
##            newquery = qry.format(state.start_date, state.end_date, state.compare, state.value)
##        else:
##            qry+=' group by uu.playerid order by kills desc;'
##            newquery = qry.format(state.start_date, state.end_date)
            
##########  Main KDR calculator with players, dates, maps and/or weapon
    elif query == 'details':
        qry = """
        select killerId as playerId, handle, sum(tot.kills) as kills, sum(tot.deaths) as deaths,
        t.tier, t.generation, t.firstname, t.lastname, t.membersince, t.location, t.kdr_year, t.maps_played from (
            SELECT {2}, killerId, 0 as deaths, count(*) as kills FROM 
                (select * from geekfest.hlstats_events_frags a where date(a.eventTime) >= '{0}' and date(a.eventTime) <= '{1}') as aa
            group by killerId, {2}
            UNION
            Select {2}, victimId, count(*) as deaths, 0 as kills FROM 
                (select * from geekfest.hlstats_events_frags b where date(b.eventTime) >= '{0}' and date(b.eventTime) <= '{1}') as bb
            group by victimId, {2}
            ) tot, geekfest.geeks t
        where tot.killerId = t.playerId
        and {2} = '{3}'
        group by playerId, {2}, handle
        order by {2}, kills desc;
        """
        newquery = qry.format(state.start_date, state.end_date, state.compare, state.value)

##########  Player Data KDR calculator with players, dates, maps and/or weapon selected by playerid

    elif query == 'playerdetails':
        qry = """
        select killerId as playerId, handle, sum(tot.kills) as kills, sum(tot.deaths) as deaths,
        t.tier, t.generation, t.firstname, t.lastname, t.membersince, t.location, {2}, t.kdr_year, t.maps_played from (
            SELECT {2}, killerId, 0 as deaths, count(*) as kills FROM 
                (select * from geekfest.hlstats_events_frags a where date(eventTime) >= '{0}' and date(eventTime) <= '{1}') as aa
            group by killerId, {2}
            UNION
            Select {2}, victimId, count(*) as deaths, 0 as kills FROM 
                (select * from geekfest.hlstats_events_frags b where date(eventTime) >= '{0}' and date(eventTime) <= '{1}') as bb
            group by victimId, {2}
            ) tot, geekfest.geeks t
        where tot.killerId = t.playerId
        group by playerId, {2}, handle
        having playerID = {3}
        order by kills desc, deaths desc;
        """
        newquery = qry.format(state.start_date, state.end_date, state.compare, state.value)

    elif query == 'playerperf':
        qry="""
        select player, handle, sum(tot.kills) as kills, sum(tot.deaths) as deaths,
        t.tier, t.generation, t.firstname, t.lastname, t.membersince, t.location, handle  from 
        ( SELECT victimId as player, 0 as deaths, count(*) as kills 
        FROM (
        select * from geekfest.hlstats_events_frags a 
        where date(eventTime) >= '{0}' and date(eventTime) <= '{1}' and killerId={2}) as aa 
        group by victimId 
        UNION 
        Select killerId as player, count(*) as deaths, 0 as kills FROM (
        select * from geekfest.hlstats_events_frags b 
        where date(eventTime) >= '{0}' and date(eventTime) <= '{1}' and victimId={2}) as bb 
        group by killerId) tot, geekfest.geeks t 
        where tot.player = t.playerId 
        group by playerId 
        order by kills desc, deaths desc;
        """        
        newquery = qry.format(state.start_date, state.end_date, state.value)
        
##########  Lookup for lists of values from main frags table
    elif query == 'values':
        qry = "select distinct {2} from geekfest.hlstats_events_frags where date(eventTime) >= '{0}' and date(eventTime) <= '{1}'"
        newquery = qry.format(state.start_date, state.end_date, state.compare)

##########  Stats associated with a single player action
    elif query == 'action':
        qry = """
            SELECT c.handle, bonus+1 as events
            FROM geekfest.hlstats_events_playeractions a, geekfest.hlstats_actions b, geekfest.geeks c 
            where a.actionId = b.id
            and a.playerId = c.playerId
            and date(eventTime) >= '{0}' and date(eventTime) <= '{1}'
            and {2}
            group by c.playerId, c.handle, b.description
            order by reward_player desc;
        """
        newquery = qry.format(state.start_date, state.end_date, state.compare)

##########  Stats associated with a count of events
    elif query == 'events':
        qry = """
            SELECT c.handle, count(*) as events
            FROM geekfest.hlstats_events_playeractions a, geekfest.geeks c 
            where a.playerId = c.playerId
            and date(eventTime) >= '{0}' and date(eventTime) <= '{1}'
            and {2}
            group by c.playerId, c.handle
            order by events desc;
        """
        newquery = qry.format(state.start_date, state.end_date, state.compare)

##########  Killer stats from frags table
    elif query == 'skills':
        qry = """
            select b.handle as player, count(*) as events
            from geekfest.hlstats_events_frags a, geeks b
            where a.killerId = b.playerId and date(eventTime) >= '{0}' and date(eventTime) <= '{1}'
            and {2}
            group by killerId, b.handle
            order by events desc;
            """
        
        newquery = qry.format(state.start_date, state.end_date, state.compare)
##########  Victim stats from core frags table        
    elif query == 'victim':
        qry = """
            select b.handle as player, count(*) as events
            from geekfest.hlstats_events_frags a, geeks b
            where a.victimId = b.playerId and date(eventTime) >= '{0}' and date(eventTime) <= '{1}'
            and {2}
            group by victimId, b.handle
            order by events desc;
            """
        
        newquery = qry.format(state.start_date, state.end_date, state.compare)

##########  Stats from events in game
    elif query == 'count':
        qry = """
            select u.handle as player, count(*) as events 
            from (select distinct weapon, b.handle
            from geekfest.hlstats_events_frags a, geekfest.geeks b
            where date(eventTime) >= '{0}' and date(eventTime) <= '{1}'
            and {2}
            ) u
            group by u.handle
            order by events desc;
            """
        newquery = qry.format(state.start_date, state.end_date, state.compare)
##########  Stats from team bonuses for awards
    elif query == 'teamscore':
        qry = """
            SELECT handle, count(*) as events
            FROM geekfest.hlstats_events_teambonuses a, geeks g, hlstats_actions b
            where a.actionId = b.id
            and a.playerid = g.playerid
            and date(eventTime) >= '{0}' and date(eventTime) <= '{1}'
            and {2}
            group by handle
            order by events desc;
            """
        newquery = qry.format(state.start_date, state.end_date, state.compare)
        

##########  Stats from team killer table
    elif query == 'tk':
        qry = """
            SELECT handle as player, count(*) as events 
            FROM geekfest.hlstats_events_teamkills a, geeks b
            where date(eventTime) >= '{0}' and date(eventTime) <= '{1}'
            and {2}
            group by handle order by events desc;
            """
        newquery = qry.format(state.start_date, state.end_date, state.compare)

##########  Distance Stats for killer
    elif query == 'distance':
        qry = """
        select handle, 
        round(sqrt(power(pos_x - pos_victim_x,2) 
        + power(pos_y - pos_victim_y,2) 
        + power(pos_z - pos_victim_z,2))/12,2) as events 
        from geekfest.hlstats_events_frags a, geeks b
        where a.killerId = b.playerId and (eventTime) >= '{0}' and date(eventTime) <= '{1}' 
        order by events {2};
            """
        newquery = qry.format(state.start_date, state.end_date, state.compare)        

##########  Distance Stats for victim
    elif query == 'surprise':
        qry = """
        select handle, 
        round(sqrt(power(pos_x - pos_victim_x,2) 
        + power(pos_y - pos_victim_y,2) 
        + power(pos_z - pos_victim_z,2))/12,2) as events 
        from geekfest.hlstats_events_frags a, geeks b
        where a.victimId = b.playerId and (eventTime) >= '{0}' and date(eventTime) <= '{1}' 
        order by events {2};
            """
        newquery = qry.format(state.start_date, state.end_date, state.compare)        

##########  Distance Stats for victim
    elif query == 'csurprise':
        qry = """
	select handle, count(innerevents) as events from (
        select handle, 
        round(sqrt(power(pos_x - pos_victim_x,2) 
        + power(pos_y - pos_victim_y,2) 
        + power(pos_z - pos_victim_z,2))/12,2) as innerevents 
        from geekfest.hlstats_events_frags a, geeks b
        where a.victimId = b.playerId and (eventTime) >= '{0}' and date(eventTime) <= '{1}' ) bb
        where {2}
        group by handle
        order by events desc;
            """
        newquery = qry.format(state.start_date, state.end_date, state.compare)
        
##########  Detail log of player events for PlayerDetails
    elif query == 'detaildetails':
        qry = """
            select killerId as playerId, victimid, eventtime, headshot, weapon, t.handle, v.handle, map, weapon as victim 
            from geekfest.hlstats_events_frags a, geekfest.geeks t, geekfest.geeks v
            where date(eventTime) >= '{0}' and date(eventTime) <= '{1}'
            and (killerid = {3} or victimid = {3})
            and {2}
            and a.killerId = t.playerid and a.victimId = v.playerid;
        """
        newquery = qry.format(state.start_date, state.end_date, state.clause, state.value)
        

#########  List of Seasons for picklist on Teams        
    elif query == 'seasons':
        qry = " select name, start_date, end_date from geekfest.team_seasons order by start_date desc"
        newquery = qry

#########  Simple lookup query        
    elif query == 'simple':
        qry = state.clause
        newquery = qry
        

#########  List of games for seasons on Teams        
    elif query == 'games':
        qry = """
            select map, a.name, teamA_wins, b.name, teamB_wins, map, date(gameDate) as gameDate
            from teams a, teams b, team_games c 
            where gameDate >='{0}' and gameDate <= '{1}'
            and c.teamA = a.idteams and c.teamB = b.idteams
            order by gameDate;
            """
        newquery = qry.format(state.start_date, state.end_date)

#########  List of players on teams for a season 
    elif query == 'teams':
        qry = """
            select name, start_date, end_date, handle
            from geeks a, team_geeks b, teams c
            where a.idgeek = b.idgeek
            and b.teamid = c.idteams
            and b.start_date <= '{0}' and b.end_date >= '{1}'
            order by name;
            """
        newquery = qry.format(state.start_date, state.end_date)
    elif query == 'pdetails':
        qry = """
            select map, weapon, headshot, eventtime, g1.handle as killer, g2.handle as victim, g1.playerid
            from hlstats_events_frags f, geeks g1, geeks g2
            where f.killerId = g1.playerid and f.victimId = g2.playerid
            and date(eventTime) >= '{0}' and date(eventTime) <= '{1}'
            and (killerid = {2} or victimid = {2})
            and {3}
            order by eventtime;
            """

        newquery = qry.format(state.start_date, state.end_date, state.value, state.compare)

#########  Load Award Values
    elif query == 'val_awards':
        if state.compare== "gfxx":
            qry = """select * from gf_awards where gfxxv = 'Y' order by class;"""
            newquery = qry
        elif state.compare != "":
            qry = """select *
                from gf_awards
                where class = '{0}'
                order by class;"""
            newquery = qry.format(state.compare)
        else:
            qry = """select * from gf_awards order by class;"""
            newquery = qry

    elif query == 'perf_data':
        qry="""select killerid, handle, sum(deaths) as deaths, sum(kills) as kills, eDate
            from ktd_stats
            where killerid = {2}
            and eDate >= '{0}' and eDate <= '{1}'
            group by handle, eDate;
            """
        newquery = qry.format(state.start_date, state.end_date, state.value)
        
    
    cnx = pymysql.connect(user=username, password=password, host=server,database=database)
    cursor = cnx.cursor()
##    print(newquery)
    cursor.execute(newquery)
    data = list(cursor.fetchall())
    cursor.close()
    cnx.close()
    return data

##def get_df():
##    query = """select handle, sum(kills) as kills, sum(deaths) as deaths, eDate from ktd_stats group by handle, eDate"""
##    df = pd.read_sql(query, cnx)                                    #Leverages dataframe to load data from database
##    return df

