USE geek;
CREATE 
    ALGORITHM = UNDEFINED 
VIEW `tiers_data` AS
    SELECT 
        UUID() AS `id`,
        `tot`.`geek_id` AS `geekid`,
        `g`.`handle` AS `player`,
        `t`.`tier_name` AS `tier`,
        `t`.`tier_id` AS `tier_id`,
        `g`.`generation_id` AS `generation`,
        CAST(`sm`.`match_date` AS DATE) AS `matchdate`,
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
        `ga`.`ADR` AS `ADR`,
        `g`.`alltime_kdr` AS `alltime_kdr`,
        `g`.`year_kdr` AS `year_kdr`,
        `g`.`last90_kdr` AS `last90_kdr`
    FROM
        ((((((SELECT 
            `f`.`geek_id` AS `geek_id`,
                `f`.`round_id` AS `round_id`,
                1 AS `kills`,
                0 AS `deaths`,
                0 AS `assists`
        FROM
            `frag` `f`
        WHERE
            (`f`.`is_teamkill` = 0) UNION ALL SELECT 
            `d`.`geek_id` AS `geek_id`,
                `d`.`round_id` AS `round_id`,
                0 AS `kills`,
                1 AS `deaths`,
                0 AS `assists`
        FROM
            `death` `d`
        WHERE
            (`d`.`is_teamkill` = 0) UNION ALL SELECT 
            `a`.`geek_id` AS `geek_id`,
                `a`.`round_id` AS `round_id`,
                0 AS `kills`,
                0 AS `deaths`,
                1 AS `assists`
        FROM
            `assist` `a`
        WHERE
            (`a`.`is_tk_assist` = 0)) `tot`
        JOIN `geek` `g` ON ((`g`.`geek_id` = `tot`.`geek_id`)))
        JOIN `tier` `t` ON ((`g`.`tier_id` = `t`.`tier_id`)))
        JOIN `geek_adr` `ga` ON ((`g`.`geek_id` = `ga`.`geek_id`)))
        JOIN `match_round` `mr` ON ((`tot`.`round_id` = `mr`.`round_id`)))
        JOIN `season_match` `sm` ON ((`mr`.`match_id` = `sm`.`match_id`)))
    GROUP BY `tot`.`geek_id` , `g`.`handle` , `t`.`tier_name` , `g`.`generation_id` , CAST(`sm`.`match_date` AS DATE) , `g`.`alltime_kdr` , `g`.`year_kdr` , `g`.`last90_kdr` , `ga`.`ADR`