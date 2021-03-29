CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `geekfest`@`%` 
    SQL SECURITY DEFINER
VIEW `match_stats` AS
    SELECT 
        `fr`.`geek_id` AS `geek_id`,
        `fr`.`match_id` AS `match_id`,
        `fr`.`handle` AS `handle`,
        `fr`.`frags` AS `frags`,
        `de`.`deaths` AS `deaths`,
        `ass`.`assists` AS `assists`,
        (`fr`.`frags` / `de`.`deaths`) AS `kdr`
    FROM
        ((((SELECT 
            `mr`.`match_id` AS `match_id`,
                `g`.`geek_id` AS `geek_id`,
                `g`.`handle` AS `handle`,
                COUNT(0) AS `frags`
        FROM
            ((`geek`.`frag` `f`
        JOIN `geek`.`geek` `g` ON ((`f`.`geek_id` = `g`.`geek_id`)))
        JOIN `geek`.`match_round` `mr` ON ((`f`.`round_id` = `mr`.`round_id`)))
        WHERE
            (`f`.`is_teamkill` = 0)
        GROUP BY `mr`.`match_id` , `g`.`geek_id` , `g`.`handle`)) `fr`
        LEFT JOIN (SELECT 
            `mr`.`match_id` AS `match_id`,
                `g`.`geek_id` AS `geek_id`,
                `g`.`handle` AS `handle`,
                COUNT(0) AS `deaths`
        FROM
            ((`geek`.`death` `d`
        JOIN `geek`.`geek` `g` ON ((`d`.`geek_id` = `g`.`geek_id`)))
        JOIN `geek`.`match_round` `mr` ON ((`d`.`round_id` = `mr`.`round_id`)))
        WHERE
            (`d`.`is_teamkill` = 0)
        GROUP BY `mr`.`match_id` , `g`.`geek_id` , `g`.`handle`) `de` ON (((`fr`.`geek_id` = `de`.`geek_id`)
            AND (`fr`.`match_id` = `de`.`match_id`))))
        LEFT JOIN (SELECT 
            `mr`.`match_id` AS `match_id`,
                `g`.`geek_id` AS `geek_id`,
                `g`.`handle` AS `handle`,
                COUNT(0) AS `assists`
        FROM
            ((`geek`.`assist` `a`
        JOIN `geek`.`geek` `g` ON ((`a`.`geek_id` = `g`.`geek_id`)))
        JOIN `geek`.`match_round` `mr` ON ((`a`.`round_id` = `mr`.`round_id`)))
        WHERE
            (`a`.`is_tk_assist` = 0)
        GROUP BY `mr`.`match_id` , `g`.`geek_id` , `g`.`handle`) `ass` ON (((`fr`.`geek_id` = `ass`.`geek_id`)
            AND (`fr`.`match_id` = `ass`.`match_id`))))
    ORDER BY `fr`.`match_id` , (`fr`.`frags` / `de`.`deaths`) DESC , `fr`.`handle`