SET SQL_SAFE_UPDATES=0;

DELETE FROM geek.geekfest_award;
DELETE FROM geek.award_category;

SET SQL_SAFE_UPDATES=1;

INSERT INTO geek.award_category(award_category_id, category_name, category_description, category_color) VALUES (1, 'Soldier', 'Good at getting frags', 'rgba(255,223,0,0.5)');
INSERT INTO geek.award_category(award_category_id, category_name, category_description, category_color) VALUES (2, 'Assassin', 'Silent but deadly', 'rgb(211,211,211)');

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







