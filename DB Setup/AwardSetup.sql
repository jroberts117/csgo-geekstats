INSERT INTO geek.award_category(category_name, category_description) VALUES ('Soldier', 'Good at getting frags');

INSERT INTO geek.geekfest_award(geekfest_award_id, award_name, award_title, award_description, award_image_path, award_category_id, award_query, award_query_type)
VALUES (1,'Kills in a row', 'The Mechanic', 'Kills in a row in a single round', 'themechanic.png', 1, 'SELECT {match}, {award}, geek_id, MAX(streak) as streak
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
ORDER BY streak DESC', 'sql');
