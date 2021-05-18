SET SQL_SAFE_UPDATES=0;

DELETE FROM geek.geekfest_award;
DELETE FROM geek.award_category;

SET SQL_SAFE_UPDATES=1;

INSERT INTO geek.award_category(award_category_id, category_name, category_description, category_color) VALUES (1, 'Soldier', 'Good at getting frags', 'rgba(255,223,0,0.5)');
INSERT INTO geek.award_category(award_category_id, category_name, category_description, category_color) VALUES (2, 'Assassin', 'Silent but deadly', 'rgb(211,211,211)');
INSERT INTO geek.award_category(award_category_id, category_name, category_description, category_color) VALUES (3, 'Specialist', 'Master of the trade', 'rgba(184, 115, 51, 0.5)');
INSERT INTO geek.award_category(award_category_id, category_name, category_description, category_color) VALUES (4, 'Hero', 'Valuable team member', 'rgb(245,245,245)');
INSERT INTO geek.award_category(award_category_id, category_name, category_description, category_color) VALUES (5, 'N00b', 'Happens to the best of us', 'rgb(255,114,111)');
INSERT INTO geek.award_category(award_category_id, category_name, category_description, category_color) VALUES (6, 'Team', 'Team achievements for all', 'rgb(168,212,198)');
INSERT INTO geek.award_category(award_category_id, category_name, category_description, category_color) VALUES (7, 'New*', 'New awards that have yet to be categorized', 'rgb(146,207,255)');

INSERT INTO geek.geekfest_award(geekfest_award_id, award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES (1,'Kills in a row', 'The Mechanic', 'Kills in a row in a single round', '/images/ribbons/4_mostkills.png', 1, 'SELECT {match}, {award}, geek_id, MAX(streak) as streak
FROM (
SELECT f.geek_id, COALESCE(lives.start_round, 0) AS life, COUNT(*) as streak FROM geek.frag f
                        JOIN geek.match_round mr on f.round_id=mr.round_id
				LEFT JOIN (SELECT d.round_id as start_round, d.geek_id, MIN(COALESCE(dupper.round_id, 999999)) as end_round FROM geek.death d
					JOIN geek.match_round mr ON d.round_id=mr.round_id
					LEFT JOIN geek.death dupper ON dupper.round_id > d.round_id AND d.geek_id=dupper.geek_id
					LEFT JOIN geek.match_round mrupper ON dupper.round_id=mrupper.round_id
					WHERE mr.match_id={match}
					GROUP BY d.round_id, d.geek_id) lives ON mr.round_id > lives.start_round AND mr.round_id <= lives.end_round AND lives.geek_id=f.geek_id
                WHERE match_id={match} AND is_teamkill=0
                GROUP BY f.geek_id, COALESCE(lives.start_round, 0)
        ORDER BY streak DESC) kstreaks
GROUP BY geek_id
ORDER BY streak DESC', 'sql', 'max');

INSERT INTO geek.geekfest_award(geekfest_award_id, award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES (2,'Total Headshots', 'John Wick', 'The number of headshots made', '/images/ribbons/4_headshot.png', 1, 
'SELECT {match}, {award}, geek_id, COUNT(*) as headshots
FROM geek.frag f
JOIN geek.match_round mr ON f.round_id=mr.round_id
WHERE f.is_headshot=1 AND f.is_teamkill=0 AND mr.match_id={match}
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(geekfest_award_id, award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES (3,'Weapons Used To Kill', 'Arms Dealer', 'The number unique items used to kill in a single match', '/images/ribbons/4_arms_dealer.png', 1, 
'SELECT {match}, {award}, geek_id, COUNT(DISTINCT item_id) AS items
FROM geek.frag f
	JOIN geek.match_round mr ON f.round_id=mr.round_id
WHERE f.is_teamkill=0 AND mr.match_id={match}
GROUP BY geek_id', 'sql', 'max');

INSERT INTO geek.geekfest_award(geekfest_award_id, award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES (4,'Blasts With A Deagle', 'Dirty Harry', 'The number of kills achieved with the Desert Eagle', '/images/ribbons/4_deagle.png', 1, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.frag f
	JOIN geek.match_round mr ON f.round_id=mr.round_id
    JOIN geek.item i ON f.item_id=i.item_id
WHERE f.is_teamkill=0 AND mr.match_id={match} AND i.name=\'deagle\'
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(geekfest_award_id, award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES (5,'Total SMG Kills', 'Say Hello to my Little Friend', 'The number of kills using a weapon from the SMG menu', '/images/ribbons/4_mac10.png', 1, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.frag f
	JOIN geek.match_round mr ON f.round_id=mr.round_id
    JOIN geek.item i ON f.item_id=i.item_id
WHERE f.is_teamkill=0 AND mr.match_id={match} AND i.category=\'SMG\'
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(geekfest_award_id, award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES (6,'Total Knife Kills', 'Et Tu Brute', 'The number of kills using a knife', '/images/ribbons/4_knife.png', 2, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.frag f
	JOIN geek.match_round mr ON f.round_id=mr.round_id
    JOIN geek.item i ON f.item_id=i.item_id
WHERE f.is_teamkill=0 AND mr.match_id={match} AND i.category=\'Knives\'
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(geekfest_award_id, award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES (7,'Total Kills With Silencer', 'Silent but Deadly', 'The number of kills with the USP, M4A1 Silencer, and MP5-SD', '/images/ribbons/1_silenced.png', 2, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.frag f
	JOIN geek.match_round mr ON f.round_id=mr.round_id
    JOIN geek.item i ON f.item_id=i.item_id
WHERE f.is_teamkill=0 AND mr.match_id={match} AND i.name IN (\'usp_silencer\', \'m4a1_silencer\', \'mp5sd\')
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(geekfest_award_id, award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES (8,'Snipes', 'Eagle Eye', 'The number of kills with ssg08', '/images/ribbons/4_ssg08.png', 2, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.frag f
	JOIN geek.match_round mr ON f.round_id=mr.round_id
    JOIN geek.item i ON f.item_id=i.item_id
WHERE f.is_teamkill=0 AND mr.match_id={match} AND i.name=\'ssg08\'
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(geekfest_award_id, award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES (9,'Pistol Kills', 'Bond, James Bond', 'The number of kills with pistols', '/images/ribbons/4_glock.png', 2, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.frag f
	JOIN geek.match_round mr ON f.round_id=mr.round_id
    JOIN geek.item i ON f.item_id=i.item_id
WHERE f.is_teamkill=0 AND mr.match_id={match} AND i.category=\'Pistols\'
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(geekfest_award_id, award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES (10,'Blasts With an AWP', 'Bazooka Joe', 'The number of kills with an AWP', '/images/ribbons/4_awp.png', 2, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.frag f
	JOIN geek.match_round mr ON f.round_id=mr.round_id
    JOIN geek.item i ON f.item_id=i.item_id
WHERE f.is_teamkill=0 AND mr.match_id={match} AND i.name=\'awp\'
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(geekfest_award_id, award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES (11,'Longest Distance Kill In Feet', 'Long Shot', 'Longest distance for a kill shot in feet (estimated in CSGO distance)', '/images/ribbons/4_awp.png', 2, 
'SELECT {match}, {award}, geek_id, MAX(distance/16) AS value
FROM geek.frag f
	JOIN geek.match_round mr ON f.round_id=mr.round_id
    JOIN geek.item i ON f.item_id=i.item_id
WHERE f.is_teamkill=0 AND mr.match_id={match}
GROUP BY geek_id', 'sql', 'max');

INSERT INTO geek.geekfest_award(geekfest_award_id, award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES (12,'Snipes With Any Sniper Rifle', 'Eagle Eye 2', 'The number of kills with any sniper rifle', '/images/ribbons/4_ssg08.png', 2, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.frag f
	JOIN geek.match_round mr ON f.round_id=mr.round_id
    JOIN geek.item i ON f.item_id=i.item_id
WHERE f.is_teamkill=0 AND mr.match_id={match} AND i.sub_category=\'Sniper Rifles\'
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(geekfest_award_id, award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES (13,'Grenade Kills', 'Ok, Boomer', 'The number of kills with the HE Grenade', '/images/ribbons/2_hegrenade.png', 3, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.frag f
	JOIN geek.match_round mr ON f.round_id=mr.round_id
    JOIN geek.item i ON f.item_id=i.item_id
WHERE f.is_teamkill=0 AND mr.match_id={match} AND i.name=\'hegrenade\'
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(geekfest_award_id, award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES (14,'Shotgun Kills', 'The Terminator', 'The number of kills with any shotgun', '/images/ribbons/2_sawedoff.png', 3, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.frag f
	JOIN geek.match_round mr ON f.round_id=mr.round_id
    JOIN geek.item i ON f.item_id=i.item_id
WHERE f.is_teamkill=0 AND mr.match_id={match} AND i.sub_category=\'Shotguns\'
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(geekfest_award_id, award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES (15,'LMG Mow Downs', 'Rambo', 'The number of kills with the negev or M249', '/images/ribbons/2_negev.png', 3, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.frag f
	JOIN geek.match_round mr ON f.round_id=mr.round_id
    JOIN geek.item i ON f.item_id=i.item_id
WHERE f.is_teamkill=0 AND mr.match_id={match} AND i.sub_category=\'LMG\'
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(geekfest_award_id, award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES (16,'Revolver Kills', 'I Wanna Be A Cowboy', 'The number of kills with the Revolver', '/images/ribbons/2_deagle.png', 3, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.frag f
	JOIN geek.match_round mr ON f.round_id=mr.round_id
    JOIN geek.item i ON f.item_id=i.item_id
WHERE f.is_teamkill=0 AND mr.match_id={match} AND i.name=\'revolver\'
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(geekfest_award_id, award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES (17,'Players Burnt To Ashes', '15 Minutes of Flame', 'The number of kills with incendiary items', '/images/ribbons/2_firebomb.png', 3, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.frag f
	JOIN geek.match_round mr ON f.round_id=mr.round_id
    JOIN geek.item i ON f.item_id=i.item_id
WHERE f.is_teamkill=0 AND mr.match_id={match} AND i.name IN (\'inferno\', \'incgrenade\', \'molotov\')
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(geekfest_award_id, award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES (18,'Taser Kills', 'Dickola Tesla', 'The number of kills with the Taser', '/images/ribbons/2_taser.png', 3, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.frag f
	JOIN geek.match_round mr ON f.round_id=mr.round_id
    JOIN geek.item i ON f.item_id=i.item_id
WHERE f.is_teamkill=0 AND mr.match_id={match} AND i.name=\'taser\'
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(geekfest_award_id, award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES (19,'Dualie Kills', 'Akimbo', 'The number of kills with dualies', '/images/ribbons/2_elite.png', 3, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.frag f
	JOIN geek.match_round mr ON f.round_id=mr.round_id
    JOIN geek.item i ON f.item_id=i.item_id
WHERE f.is_teamkill=0 AND mr.match_id={match} AND i.name=\'elite\'
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(geekfest_award_id, award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES (20,'Deaths By A Team Member', 'Mistaken Identity', 'The number of times killed by a teammate', '/images/ribbons/1_teamkills.png', 4, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.death d
	JOIN geek.match_round mr ON d.round_id=mr.round_id
WHERE d.is_teamkill=1 AND mr.match_id={match}
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(geekfest_award_id, award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES (21,'Picked Up The Bomb', 'Try Hard', 'The number of times the player picked up the bomb', '/images/ribbons/1_planted_the_bomb.png', 4, 
'SELECT {match}, {award}, geek_id, COUNT(*) as value 
FROM geek.player_event_action pea
	JOIN geek.action a ON pea.action_id=a.action_id
	JOIN geek.match_round mr ON pea.round_id=mr.round_id
WHERE a.code=\'Got_The_Bomb\' AND mr.match_id={match}
GROUP BY geek_id', 'sql', 'sum');


INSERT INTO geek.geekfest_award(geekfest_award_id, award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES (22,'Alive To See Enemy Eliminated', 'Last Man Standing', 'The number of times the player was still alive when all enemies were eliminated', '/images/ribbons/1_standaard.png', 4, 
'SELECT {match}, {award}, g.geek_id, COUNT(*) AS value FROM geek.team_event_action tea
	JOIN geek.action a ON tea.action_id=a.action_id
    JOIN geek.match_round mr ON tea.round_id=mr.round_id
    JOIN geek.geek g
WHERE a.code IN (\'SFUI_Notice_Terrorists_Win\', \'SFUI_Notice_CTs_Win\')
	AND (EXISTS (SELECT 1 FROM geek.frag WHERE geek_id=g.geek_id AND round_id=mr.round_id)
		OR EXISTS (SELECT 1 FROM geek.buy WHERE geek_id=g.geek_id AND round_id=mr.round_id))
	AND NOT EXISTS (SELECT 1 FROM geek.death WHERE geek_id=g.geek_id AND round_id=mr.round_id)
	AND mr.match_id={match}
GROUP BY g.geek_id', 'sql', 'sum');


INSERT INTO geek.geekfest_award(geekfest_award_id, award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES (23,'Round MVP Awards', 'MVP', 'The number of MVP awards a player received', '/images/ribbons/1_round_mvp.png', 4, 
'SELECT {match}, {award}, geek_id, COUNT(*) as value 
FROM geek.player_event_action pea
	JOIN geek.action a ON pea.action_id=a.action_id
	JOIN geek.match_round mr ON pea.round_id=mr.round_id
WHERE a.code=\'round_mvp\' AND mr.match_id={match}
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES ('Total Deaths', 'Red Shirt', 'The amount of total times a player died', '/images/ribbons/6_redshirt.png', 5, 
'SELECT {match}, {award},  geek_id, COUNT(*) AS value
FROM geek.death d
	JOIN geek.match_round mr ON d.round_id=mr.round_id
WHERE d.is_teamkill=0 AND mr.match_id={match}
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES ('Shots To The Head', 'Mailboxhead', 'The number of times a player was killed with a headshot', '/images/ribbons/6_headshot.png', 5, 
'SELECT {match}, {award},  geek_id, COUNT(*) AS value
FROM geek.death d
	JOIN geek.match_round mr ON d.round_id=mr.round_id
WHERE d.is_teamkill=0 AND mr.match_id={match} AND d.is_headshot=1
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES ('Weapons Killed By', 'Target Practice', 'The number unique items a player was killed with in a single match', '/images/ribbons/6_target.png', 5, 
'SELECT {match}, {award}, geek_id, COUNT(DISTINCT item_id) AS items
FROM geek.death d
	JOIN geek.match_round mr ON d.round_id=mr.round_id
WHERE d.is_teamkill=0 AND mr.match_id={match}
GROUP BY geek_id', 'sql', 'max');

INSERT INTO geek.geekfest_award(award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES ('Team Kills', 'Tonya Harding', 'The number of times a player killed a teammate', '/images/ribbons/6_suicide.png', 5, 
'SELECT {match}, {award},  geek_id, COUNT(*) AS value
FROM geek.frag f
	JOIN geek.match_round mr ON f.round_id=mr.round_id
WHERE f.is_teamkill=1 AND mr.match_id={match}
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES ('Closest Death In Feet', 'SURPRISE!', 'Closest distance of a death in feet (estimated in CSGO distance)', '/images/ribbons/6_killed_a_hostage.png', 5, 
'SELECT {match}, {award}, geek_id, MIN(distance/16) AS value
FROM geek.death d
	JOIN geek.match_round mr ON d.round_id=mr.round_id
WHERE d.is_teamkill=0 AND mr.match_id={match}
GROUP BY geek_id', 'sql', 'min');

INSERT INTO geek.geekfest_award(award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES ('Killed From Afar', 'Hide In Plain Sight', 'The number of times player was killed from greater than 100 feet (estimated in CSGO distance)', '/images/ribbons/6_awp.png', 5, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.death d
	JOIN geek.match_round mr ON d.round_id=mr.round_id
WHERE d.is_teamkill=0 AND mr.match_id={match} AND (distance/16)>100
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES ('Deaths By Grenade', 'Wrong Place, Wrong Time', 'The number of times player was killed by any item in the grenade menu', '/images/ribbons/6_hegrenade.png', 5, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.death d
	JOIN geek.match_round mr ON d.round_id=mr.round_id
    JOIN geek.item i on d.item_id=i.item_id
WHERE d.is_teamkill=0 AND mr.match_id={match} AND i.sub_category=\'Grenades\'
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES ('Deaths By Zeus', 'Fried', 'The number of times player was killed with a taser', '/images/ribbons/6_taser.png', 5, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.death d
	JOIN geek.match_round mr ON d.round_id=mr.round_id
    JOIN geek.item i on d.item_id=i.item_id
WHERE d.is_teamkill=0 AND mr.match_id={match} AND i.name=\'taser\'
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES ('Tazed, Stabbed, Burned Or Blown Up', 'Humiliated', 'The number of times player was killed with flame, taser, grenade, or knife', '/images/ribbons/6_killed_a_hostage.png', 5, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.death d
	JOIN geek.match_round mr ON d.round_id=mr.round_id
    JOIN geek.item i on d.item_id=i.item_id
WHERE d.is_teamkill=0 AND mr.match_id={match} AND 
	(i.name=\'taser\' OR i.sub_category=\'Grenades\' OR i.category=\'Knives\' OR i.name=\'inferno\')
GROUP BY geek_id', 'sql', 'sum');


INSERT INTO geek.geekfest_award(award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES ('Failed Bomb Carries', 'Failed To Deliver', 'The number of times a player had the bomb but failed to plant', '/images/ribbons/3_planted_the_bomb.png', 6, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.player_event_action pea
	JOIN geek.match_round mr ON pea.round_id=mr.round_id
    JOIN geek.action a ON pea.action_id=a.action_id
WHERE a.code=\'Got_The_Bomb\' AND mr.match_id={match} AND 
	NOT EXISTS (SELECT 1 FROM geek.player_event_action ipea
				JOIN geek.action ia ON ipea.action_id=ia.action_id
				WHERE ipea.round_id=pea.round_id AND ipea.geek_id=pea.geek_id AND ia.code=\'Planted_The_Bomb\')
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES ('Bomb Plants', 'Saboteur', 'The number of times a player planted the bomb', '/images/ribbons/3_planted_the_bomb.png', 6, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.player_event_action pea
	JOIN geek.match_round mr ON pea.round_id=mr.round_id
    JOIN geek.action a ON pea.action_id=a.action_id
WHERE a.code=\'Planted_The_Bomb\' AND mr.match_id={match} 
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES ('Hostages Rescued', 'Rescue Hero', 'The number of times a player rescued a hostage', '/images/ribbons/3_rescued_a_hostage.png', 6, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.player_event_action pea
	JOIN geek.match_round mr ON pea.round_id=mr.round_id
    JOIN geek.action a ON pea.action_id=a.action_id
WHERE a.code=\'Rescued_A_Hostage\' AND mr.match_id={match} 
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES ('Bombs Defused', 'MacGyver', 'The number of times a player defused the bomb', '/images/ribbons/3_defused_the_bomb.png', 6, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.player_event_action pea
	JOIN geek.match_round mr ON pea.round_id=mr.round_id
    JOIN geek.action a ON pea.action_id=a.action_id
WHERE a.code=\'Defused_The_Bomb\' AND mr.match_id={match} 
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES ('Attempts To Rescue', 'Hero Wannabe', 'The number of times a player attempted to rescue a hostage (includes both failed and successful attempts)', '/images/ribbons/3_rescued_a_hostage.png', 6, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.player_event_action pea
	JOIN geek.match_round mr ON pea.round_id=mr.round_id
    JOIN geek.action a ON pea.action_id=a.action_id
WHERE a.code=\'Touched_A_Hostage\' AND mr.match_id={match} 
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES ('No Kit Defusal Attempts', 'Not A Boyscout', 'The number of times a player attempted to defuse the bomb without a kit', '/images/ribbons/3_rescued_a_hostage.png', 6, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.player_event_action pea
	JOIN geek.match_round mr ON pea.round_id=mr.round_id
    JOIN geek.action a ON pea.action_id=a.action_id
WHERE a.code=\'Begin_Bomb_Defuse_Without_Kit\' AND mr.match_id={match} 
GROUP BY geek_id', 'sql', 'sum');



INSERT INTO geek.geekfest_award(award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES ('Most Money Spent', 'Big Spender', 'The amount of money spent', '/images/ribbons/1_standaard.png', 7, 
'SELECT {match}, {award}, geek_id, SUM(cost) AS value
FROM geek.buy b
	JOIN geek.match_round mr ON b.round_id=mr.round_id
    JOIN geek.item i ON b.item_id=i.item_id
WHERE mr.match_id={match}
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES ('Total Penetration Kills', 'Wall Banger', 'The total number of penetration kills made', '/images/ribbons/1_standaard.png', 7, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.frag f
	JOIN geek.match_round mr ON f.round_id=mr.round_id
    JOIN geek.item i ON f.item_id=i.item_id
WHERE f.is_teamkill=0 AND mr.match_id={match} AND f.is_penetration=1
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES ('Total Time Enemies Flashed', 'The Neuralyzer', 'The total time player blinded enemies with a flashbang', '/images/ribbons/1_standaard.png', 7, 
'SELECT {match}, {award}, blinding_player_id, SUM(duration) AS value
FROM geek.blind b
	JOIN geek.match_round mr ON b.round_id=mr.round_id
WHERE b.is_team_blind=0 AND mr.match_id={match}
GROUP BY blinding_player_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES ('Total Time Allies Flashed', 'The Flasher', 'The total time player blinded allies with a flashbang', '/images/ribbons/1_standaard.png', 7, 
'SELECT {match}, {award}, blinding_player_id, SUM(duration) AS value
FROM geek.blind b
	JOIN geek.match_round mr ON b.round_id=mr.round_id
WHERE b.is_team_blind=1 AND mr.match_id={match}
GROUP BY blinding_player_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES ('Total Time Flashed', 'Ray Charles', 'The total time player was blinded by a flashbang (from either enemies or allies)', '/images/ribbons/1_standaard.png', 7, 
'SELECT {match}, {award}, blinded_player_id, SUM(duration) AS value
FROM geek.blind b
	JOIN geek.match_round mr ON b.round_id=mr.round_id
WHERE mr.match_id={match}
GROUP BY blinded_player_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES ('Dream Killer', 'Freddy Krueger', 'The total times a player has killed Dream', '/images/ribbons/1_standaard.png', 7, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.frag f
	JOIN geek.match_round mr ON f.round_id=mr.round_id
WHERE mr.match_id={match} AND victim_id=13 AND f.is_teamkill=0
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES ('Dream\'s Bitch', 'Master Baiter', 'The total times a player has been killed by Dream', '/images/ribbons/1_standaard.png', 7, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.death d
	JOIN geek.match_round mr ON d.round_id=mr.round_id
WHERE mr.match_id={match} AND killer_id=13 AND d.is_teamkill=0
GROUP BY geek_id', 'sql', 'sum');

INSERT INTO geek.geekfest_award(award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type, award_value_type)
VALUES ('Stabs, Nades, and Tazes', 'Ninja', 'The number of times player killed with flame, taser, grenade, or knife', '/images/ribbons/1_standaard.png', 7, 
'SELECT {match}, {award}, geek_id, COUNT(*) AS value
FROM geek.frag f
	JOIN geek.match_round mr ON f.round_id=mr.round_id
    JOIN geek.item i on f.item_id=i.item_id
WHERE f.is_teamkill=0 AND mr.match_id={match} AND 
	(i.name=\'taser\' OR i.sub_category=\'Grenades\' OR i.category=\'Knives\' OR i.name=\'inferno\')
GROUP BY geek_id', 'sql', 'sum');





