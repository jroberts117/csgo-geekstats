CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `geekfest`@`%` 
    SQL SECURITY DEFINER
VIEW `frag_details` AS
    SELECT 
        `g`.`geek_id` AS `id`,
        CAST(`sm`.`match_date` AS DATE) AS `match_date`,
        `sm`.`match_date` AS `match_datetime`,
        IF(ISNULL(`g`.`is_member`),
            CONCAT('BOT_', `g`.`handle`),
            `g`.`handle`) AS `killer`,
        IF(ISNULL(`v`.`is_member`),
            CONCAT('BOT_', `v`.`handle`),
            `v`.`handle`) AS `victim`,
        `v`.`geek_id` AS `victim_id`,
        `sm`.`map` AS `map`,
        `i`.`decscription` AS `weapon`,
        'n/a' AS `partner`,
        'kill' AS `type`
    FROM
        (((((`geek` `g`
        JOIN `frag` `f` ON ((`g`.`geek_id` = `f`.`geek_id`)))
        JOIN `match_round` `mr` ON ((`mr`.`round_id` = `f`.`round_id`)))
        JOIN `season_match` `sm` ON ((`mr`.`match_id` = `sm`.`match_id`)))
        JOIN `item` `i` ON ((`i`.`item_id` = `f`.`item_id`)))
        JOIN `geek` `v` ON ((`v`.`geek_id` = `f`.`victim_id`)))
    WHERE
        (`f`.`is_teamkill` = 0) 
    UNION ALL SELECT 
        `g`.`geek_id` AS `id`,
        CAST(`sm`.`match_date` AS DATE) AS `match_date`,
        `sm`.`match_date` AS `match_datetime`,
        IF(ISNULL(`g`.`is_member`),
            CONCAT('BOT_', `g`.`handle`),
            `g`.`handle`) AS `killer`,
        'n/a' AS `victim`,
        0 AS `victim_id`,
        `sm`.`map` AS `map`,
        'n/a' AS `weapon`,
        `p`.`handle` AS `partner`,
        'assist' AS `type`
    FROM
        ((((`geek` `g`
        JOIN `assist` `a` ON ((`g`.`geek_id` = `a`.`geek_id`)))
        JOIN `match_round` `mr` ON ((`mr`.`round_id` = `a`.`round_id`)))
        JOIN `season_match` `sm` ON ((`mr`.`match_id` = `sm`.`match_id`)))
        JOIN `geek` `p` ON ((`p`.`geek_id` = `a`.`killing_player_id`)))