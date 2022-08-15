# Update maps table with all maps
insert into map (map)
select distinct map from season_match where map not in (select distinct map from map) and map != 'None';

# update the types of maps
update map set type = 'defusal' where left(map,2) = 'de';
update map set type = 'hostage' where left(map,2) = 'cs';

# add map_id column and fk to season_match
ALTER TABLE `geek`.`season_match` 
ADD COLUMN `map_id` INT NULL AFTER `team_winner`;

ALTER TABLE `geek`.`season_match` 
ADD INDEX `season_match_fk_3_idx` (`map_id` ASC) VISIBLE;
;
ALTER TABLE `geek`.`season_match` 
ADD CONSTRAINT `season_match_fk_3`
  FOREIGN KEY (`map_id`)
  REFERENCES `geek`.`map` (`idmap`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

# update data in season_match table to link maps
update season_match sm
join map m on sm.map = m.map
set sm.map_id = m.idmap;

# Create map_data view
CREATE 
    ALGORITHM = UNDEFINED 
VIEW `map_data` AS
    SELECT 
        `sm`.`map` AS `map`,
        CAST(`sm`.`match_date` AS DATE) AS `match_date`,
        `mr`.`win_side` AS `win_side`,
        `m`.`type` AS `type`,
        `m`.`theme` AS `theme`,
        `m`.`votescore` AS `votescore`
    FROM
        ((`season_match` `sm`
        JOIN `match_round` `mr` ON ((`sm`.`match_id` = `mr`.`match_id`)))
        JOIN `map` `m` ON ((`sm`.`map_id` = `m`.`idmap`)));
