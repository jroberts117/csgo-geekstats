select
	 UUID() AS `id`, tot.geek_id, 
        `g`.`handle` AS `player`,
        `t`.`tier_name` AS `tier`,
        `g`.`generation_id` AS `generation`,
        CAST(`tot`.`match_date` AS DATE) AS `matchdate`,
        sum(kills) as kills, sum(deaths) as deaths, sum(assists) as assists,
        IF((SUM(`tot`.`deaths`) = 0),
            999,
            ROUND((SUM(`tot`.`kills`) / SUM(`tot`.`deaths`)),
                    2)) AS `KDR`,
        IF((SUM(`tot`.`deaths`) = 0),
            999,
            ROUND(((SUM(`tot`.`kills`) + (SUM(`tot`.`assists`) * 0.25)) / SUM(`tot`.`deaths`)),
                    2)) AS `aKDR`,
        `g`.`alltime_kdr` AS `alltime_kdr`,
        `g`.`year_kdr` AS `year_kdr`,
        `g`.`last90_kdr` AS `last90_kdr`

from
(
	SELECT 
					`f`.`geek_id` AS `geek_id`,
					f.round_id,
                    sm.match_date,
					1 AS `kills`,
					0 AS `deaths`,
					0 AS `assists`
			FROM
				`geek`.`frag` `f`
                JOIN `geek`.`match_round` `mr` ON (`f`.`round_id` = `mr`.`round_id`)
				JOIN `geek`.`season_match` `sm` ON (`mr`.`match_id` = `sm`.`match_id`)

			WHERE
				(`f`.`is_teamkill` = 0) 
			UNION ALL 
			SELECT 
					`d`.`geek_id` AS `geek_id`,
					d.round_id,
                    sm.match_date,
					0 AS `kills`,
					1 AS `deaths`,
					0 AS `assists`
			FROM
				`geek`.`death` `d` 
                JOIN `geek`.`match_round` `mr` ON (`d`.`round_id` = `mr`.`round_id`)
				JOIN `geek`.`season_match` `sm` ON (`mr`.`match_id` = `sm`.`match_id`)

			WHERE
				(`d`.`is_teamkill` = 0)
			UNION ALL 
			SELECT 
					`a`.`geek_id` AS `geek_id`,
					a.round_id,
                    sm.match_date,
					0 AS `kills`,
					0 AS `deaths`,
					1 AS `assists`
			FROM
			`geek`.`assist` `a` 
            JOIN `geek`.`match_round` `mr` ON (`a`.`round_id` = `mr`.`round_id`)
			JOIN `geek`.`season_match` `sm` ON (`mr`.`match_id` = `sm`.`match_id`)

			WHERE
				(`a`.`is_tk_assist` = 0)
) tot
        JOIN geek.geek g ON g.geek_id = tot.geek_id
        JOIN `geek`.`tier` `t` ON (`g`.`tier_id` = `t`.`tier_id`)
        
group by geek_id,`g`.`handle` ,
        `t`.`tier_name` ,
        `g`.`generation_id` ,
        CAST(`tot`.`match_date` AS DATE),
		`g`.`alltime_kdr`,
        `g`.`year_kdr`,
        `g`.`last90_kdr`
