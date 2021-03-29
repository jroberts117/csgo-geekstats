CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `geekfest`@`%` 
    SQL SECURITY DEFINER
VIEW `team_wins` AS
    SELECT 
        `wins`.`match_id` AS `id`,
        CAST(`wins`.`match_date` AS DATE) AS `match_date`,
        `wins`.`map` AS `map`,
        `wins`.`team_name` AS `team_name`,
        SUM(`wins`.`wins`) AS `wins`
    FROM
        (SELECT 
            `ma`.`match_id` AS `match_id`,
                `ma`.`match_date` AS `match_date`,
                `ma`.`map` AS `map`,
                `t1`.`name` AS `team_name`,
                COUNT(0) AS `wins`
        FROM
            (((`geek`.`season_match` `ma`
        JOIN `geek`.`season` `s` ON ((`ma`.`season_id` = `s`.`season_id`)))
        JOIN `geek`.`match_round` `mr` ON ((`ma`.`match_id` = `mr`.`match_id`)))
        JOIN `geek`.`team` `t1` ON ((`mr`.`ct_team_id` = `t1`.`team_id`)))
        WHERE
            (`mr`.`win_side` = 'CT')
        GROUP BY `ma`.`match_id` , `ma`.`match_date` , `ma`.`map` , `team_name` UNION SELECT 
            `ma`.`match_id` AS `match_id`,
                `ma`.`match_date` AS `match_date`,
                `ma`.`map` AS `map`,
                `t2`.`name` AS `team_name`,
                COUNT(0) AS `wins`
        FROM
            (((`geek`.`season_match` `ma`
        JOIN `geek`.`season` `s` ON ((`ma`.`season_id` = `s`.`season_id`)))
        JOIN `geek`.`match_round` `mr` ON ((`ma`.`match_id` = `mr`.`match_id`)))
        JOIN `geek`.`team` `t2` ON ((`mr`.`t_team_id` = `t2`.`team_id`)))
        WHERE
            (`mr`.`win_side` = 'TERRORIST')
        GROUP BY `ma`.`match_id` , `ma`.`match_date` , `ma`.`map` , `team_name`) `wins`
    GROUP BY `wins`.`match_date` , `wins`.`map` , `wins`.`team_name` , `wins`.`match_id`