USE geek;
CREATE ALGORITHM=UNDEFINED VIEW `geek_adr` 
AS with `damage_order` 
as (select `damage`.`damage_id` AS `damage_id`,`damage`.`round_id` AS `round_id`,`damage`.`victim_id` AS `victim_id`,`damage`.`health_remaining` AS `health_remaining`
	, rank() OVER (PARTITION BY `damage`.`round_id`,`damage`.`victim_id` ORDER BY `damage`.`health_remaining` desc )  AS `dmg_order` from `damage`)
    , `round_count` as (select `mr`.`match_id` AS `match_id`,count(0) AS `num_rounds` from `match_round` `mr` group by `mr`.`match_id`) 
    select `ms`.`geek_id` AS `geek_id`,`ms`.`handle` AS `handle`,`sm`.`match_date` AS `match_date`
    ,sum((0.5 * ((`dmg`.`damage_health` + coalesce(`doB`.`health_remaining`,100)) - abs((`dmg`.`damage_health` - coalesce(`doB`.`health_remaining`,100)))))) AS `total_damage`
    ,max(`rc`.`num_rounds`) AS `number_of_rounds`,(sum((0.5 * ((`dmg`.`damage_health` + coalesce(`doB`.`health_remaining`,100)) - abs((`dmg`.`damage_health` - coalesce(`doB`.`health_remaining`,100)))))) / max(`rc`.`num_rounds`)) AS `ADR`
    ,`mr`.`match_id` AS `match_id`,(sum(`ms`.`frags`) / sum(`ms`.`deaths`)) AS `kdr` 
    from 
    ((((((`damage` `dmg` 
			join `match_round` `mr` on((`dmg`.`round_id` = `mr`.`round_id`))) 
            join `damage_order` `doA` on((`dmg`.`damage_id` = `doA`.`damage_id`))) 
            join `season_match` `sm` on((`mr`.`match_id` = `sm`.`match_id`))) 
            left join `damage_order` `doB` on(((`doA`.`round_id` = `doB`.`round_id`) and (`doA`.`victim_id` = `doB`.`victim_id`) and (`doB`.`dmg_order` = (`doA`.`dmg_order` - 1))))) 
            join `match_stats` `ms` on(((`dmg`.`geek_id` = `ms`.`geek_id`) and (`mr`.`match_id` = `ms`.`match_id`)))) 
            join `round_count` `rc` on((`mr`.`match_id` = `rc`.`match_id`))) 
	group by `mr`.`match_id`,`ms`.`handle`,`ms`.`geek_id`,`sm`.`match_date`
