CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `geekfest`@`localhost` 
    SQL SECURITY DEFINER
VIEW `geek`.`tiers_data` AS
    SELECT 
        UUID() AS `id`,
        `tot`.`geek_id` AS `geekid`,
        `tot`.`player` AS `player`,
        `tot`.`tier` AS `tier`,
        `tot`.`generation_id` AS `generation`,
        `tot`.`matchdate` AS `matchdate`,
        SUM(`tot`.`kills`) AS `kills`,
        SUM(`tot`.`deaths`) AS `deaths`,
        SUM(`tot`.`assists`) AS `assists`,
        IF((SUM(`tot`.`deaths`) = 0),
            999,
            ROUND((SUM(`tot`.`kills`) / SUM(`tot`.`deaths`)),
                    2)) AS `KDR`,
        IF((SUM(`tot`.`deaths`) = 0),
            999,
            ROUND(((SUM(`tot`.`kills`) + (SUM(`tot`.`assists`) * 0.25)) / SUM(`tot`.`deaths`)),
                    2)) AS `aKDR`,
        `tot`.`alltime_kdr` AS `alltime_kdr`,
        `tot`.`year_kdr` AS `year_kdr`,
        `tot`.`last90_kdr` AS `last90_kdr`
    FROM
        (SELECT 
            `g`.`handle` AS `player`,
                `g`.`geek_id` AS `geek_id`,
                `g`.`generation_id` AS `generation_id`,
                `g`.`alltime_kdr` AS `alltime_kdr`,
                `g`.`year_kdr` AS `year_kdr`,
                `g`.`last90_kdr` AS `last90_kdr`,
                `t`.`tier_name` AS `tier`,
                CAST(`sm`.`match_date` AS DATE) AS `matchdate`,
                COUNT(`f`.`frag_id`) AS `kills`,
                0 AS `deaths`,
                0 AS `assists`
        FROM
            ((((`geek`.`geek` `g`
        JOIN `geek`.`frag` `f` ON ((`g`.`geek_id` = `f`.`geek_id`)))
        JOIN `geek`.`tier` `t` ON ((`g`.`tier_id` = `t`.`tier_id`)))
        JOIN `geek`.`match_round` `mr` ON ((`f`.`round_id` = `mr`.`round_id`)))
        JOIN `geek`.`season_match` `sm` ON ((`mr`.`match_id` = `sm`.`match_id`)))
        WHERE
            (`f`.`is_teamkill` = 0)
        GROUP BY `g`.`handle` , `sm`.`match_date` , `g`.`geek_id` UNION ALL SELECT 
            `g`.`handle` AS `player`,
                `g`.`geek_id` AS `geek_id`,
                `g`.`generation_id` AS `generation_id`,
                `g`.`alltime_kdr` AS `alltime_kdr`,
                `g`.`year_kdr` AS `year_kdr`,
                `g`.`last90_kdr` AS `last90_kdr`,
                `t`.`tier_name` AS `tier`,
                CAST(`sm`.`match_date` AS DATE) AS `matchdate`,
                0 AS `kills`,
                COUNT(`d`.`death_id`) AS `deaths`,
                0 AS `assists`
        FROM
            ((((`geek`.`geek` `g`
        JOIN `geek`.`death` `d` ON ((`g`.`geek_id` = `d`.`geek_id`)))
        JOIN `geek`.`tier` `t` ON ((`g`.`tier_id` = `t`.`tier_id`)))
        JOIN `geek`.`match_round` `mr` ON ((`d`.`round_id` = `mr`.`round_id`)))
        JOIN `geek`.`season_match` `sm` ON ((`mr`.`match_id` = `sm`.`match_id`)))
        WHERE
            (`d`.`is_teamkill` = 0)
        GROUP BY `g`.`handle` , `sm`.`match_date` , `g`.`geek_id` UNION ALL SELECT 
            `g`.`handle` AS `player`,
                `g`.`geek_id` AS `geek_id`,
                `g`.`generation_id` AS `generation_id`,
                `g`.`alltime_kdr` AS `alltime_kdr`,
                `g`.`year_kdr` AS `year_kdr`,
                `g`.`last90_kdr` AS `last90_kdr`,
                `t`.`tier_name` AS `tier`,
                CAST(`sm`.`match_date` AS DATE) AS `matchdate`,
                0 AS `kills`,
                0 AS `deaths`,
                COUNT(`a`.`assist_id`) AS `assists`
        FROM
            ((((`geek`.`geek` `g`
        JOIN `geek`.`assist` `a` ON ((`g`.`geek_id` = `a`.`geek_id`)))
        JOIN `geek`.`tier` `t` ON ((`g`.`tier_id` = `t`.`tier_id`)))
        JOIN `geek`.`match_round` `mr` ON ((`a`.`round_id` = `mr`.`round_id`)))
        JOIN `geek`.`season_match` `sm` ON ((`mr`.`match_id` = `sm`.`match_id`)))
        WHERE
            (`a`.`is_tk_assist` = 0)
        GROUP BY `g`.`handle` , `sm`.`match_date` , `g`.`geek_id`) `tot`
    GROUP BY `tot`.`matchdate` , `tot`.`tier` , `tot`.`player` , `tot`.`geek_id` , `tot`.`generation_id`
    ORDER BY `tot`.`matchdate` DESC