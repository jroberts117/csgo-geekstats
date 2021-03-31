CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `geekfest`@`%` 
    SQL SECURITY DEFINER
VIEW `geek_info` AS
    SELECT 
        `g`.`geek_id` AS `id`,
        `td`.`player` AS `player`,
        `td`.`tier` AS `tier`,
        `gn`.`generation_name` AS `generation`,
        `g`.`location` AS `location`,
        `g`.`member_since` AS `member_since`,
        COUNT(0) AS `matches`,
        `td`.`kills` AS `kills`,
        SUM(`td`.`deaths`) AS `deaths`,
        SUM(`td`.`assists`) AS `assists`,
        IF((SUM(`td`.`deaths`) = 0),
            999,
            ROUND((SUM(`td`.`kills`) / SUM(`td`.`deaths`)),
                    2)) AS `KDR`,
        IF((SUM(`td`.`deaths`) = 0),
            999,
            ROUND(((SUM(`td`.`kills`) + (SUM(`td`.`assists`) * 0.25)) / SUM(`td`.`deaths`)),
                    2)) AS `aKDR`,
        ROUND(((TO_DAYS(NOW()) - TO_DAYS(`g`.`member_since`)) / 365),
                1) AS `tenure`
    FROM
        ((`geek`.`geek` `g`
        JOIN `geek`.`tiers_data` `td` ON ((`g`.`geek_id` = `td`.`geekid`)))
        JOIN `geek`.`generation` `gn` ON ((`gn`.`generation_id` = `g`.`generation_id`)))
    GROUP BY `td`.`player` , `td`.`tier` , `gn`.`generation_name` , `g`.`location`