# ELIMINATE DUPLICATE MAP ENTRIES IN MAP TABLE BEFORE STARTING!!!!


# Count of number of plays by map
UPDATE map m
INNER JOIN (
	select map_id, map, count(*) as plays
	from season_match
	where map != 'None'
	group by map, map_id) as sm
ON sm.map_id = m.idmap
SET m.plays = sm.plays;

# Count of number of season plays by map
UPDATE map m
INNER JOIN (
	select map_id, map, count(*) as s_plays
	from season_match
	where map != 'None' and season_id is not null
	group by map, map_id) as sm
ON m.idmap = sm.map_id
SET m.s_plays = sm.s_plays;

# Count of wins by side
UPDATE map m
INNER JOIN (
	select map_id, map, win_side, count(*) as wins from map_data
	where win_side = 'TERRORIST'
	group by map, win_side, map_id) as md
ON m.idmap = md.map_id
SET m.t_wins = md.wins; 

UPDATE map m
INNER JOIN (
	select map_id, map, win_side, count(*) as wins from map_data
	where win_side = 'CT'
	group by map, win_side, map_id) as md
ON m.idmap = md.map_id
SET m.ct_wins = md.wins; 

# Days since last play
UPDATE map m
INNER JOIN (
	select map_id, DATEDIFF(now(),max(match_date)) as last_play, map
	from season_match
	where map !='None' and map_id is not null
	group by map_id, map) as sm
ON m.idmap = sm.map_id
SET m.last_play = sm.last_play;

# Update Theme for nulls
update map m
set m.theme = 'not specified'
where m.theme is null;

# Update map scores with new metascore
update map
set metascore = round(((votescore+2)/4)*100,0)
where votescore is not null;
 

# FOR USE INSIDE OF DJANGO TO ONLY GET TOP values
# Top Geeks by Map
select map, killer, count(victim) as kills
from frag_details
where type='kill'
group by map, killer
order by map, kills desc;

# Top Guns by Map
select map, weapon, count(victim) as kills
from frag_details
where type='kill'
group by map, weapon
order by map, kills desc;

# Specific Weapon by Map
select map, weapon, count(victim) as kills
from frag_details
where type='kill' and weapon in ('knife')
group by map, weapon
order by map, kills desc;

# Update map_data view to have map_id
CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `geekfest`@`%` 
    SQL SECURITY DEFINER
VIEW `map_data` AS
    SELECT 
        `m`.`idmap` AS `map_id`,
        `sm`.`map` AS `map`,
        CAST(`sm`.`match_date` AS DATE) AS `match_date`,
        `mr`.`win_side` AS `win_side`,
        `m`.`type` AS `type`,
        `m`.`theme` AS `theme`,
        `m`.`votescore` AS `votescore`
    FROM
        ((`season_match` `sm`
        JOIN `match_round` `mr` ON ((`sm`.`match_id` = `mr`.`match_id`)))
        JOIN `map` `m` ON ((`sm`.`map_id` = `m`.`idmap`)))
