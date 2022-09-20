-- Setup cascade delete on TEAM table
ALTER TABLE `geek`.`team` 
DROP FOREIGN KEY `team_ibfk_3`;
ALTER TABLE `geek`.`team` 
ADD CONSTRAINT `team_ibfk_3`
  FOREIGN KEY (`season_id`)
  REFERENCES `geek`.`season` (`season_id`)
  ON DELETE CASCADE;

-- Add Avatar field to GEEK table
ALTER TABLE `geek`.`geek` 
ADD COLUMN `avatar` VARCHAR(100) NULL DEFAULT NULL AFTER `geek_code`;

-- Recreate TEAM_GEEK table with new fields and FKs
DROP table `geek`.`team_geek`;

CREATE TABLE `team_geek` (
  `teamgeek_id` int NOT NULL AUTO_INCREMENT,
  `geek_id` int DEFAULT NULL,
  `team_id` int DEFAULT NULL,
  `tier_id` int DEFAULT NULL,
  PRIMARY KEY (`teamgeek_id`),
  KEY `team_id` (`team_id`),
  KEY `team_geek_fk_3_idx` (`tier_id`),
  KEY `team_geek_ibfk_1` (`geek_id`),
  CONSTRAINT `team_geek_fk_3` FOREIGN KEY (`tier_id`) REFERENCES `tier` (`tier_id`),
  CONSTRAINT `team_geek_ibfk_1` FOREIGN KEY (`geek_id`) REFERENCES `geek` (`geek_id`),
  CONSTRAINT `team_geek_ibfk_2` FOREIGN KEY (`team_id`) REFERENCES `team` (`team_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1528 DEFAULT CHARSET=latin1;

-- Create Season_wins view
CREATE 
    ALGORITHM = UNDEFINED 
VIEW `season_wins` AS
    SELECT 
        `sm`.`match_date` AS `match_date`,
        `sm`.`match_id` AS `match_id`,
        `sm`.`map` AS `map`,
        `mr`.`round_id` AS `round_id`,
        `mr`.`win_side` AS `win_side`,
        `s`.`name` AS `season`,
        (CASE
            WHEN (`mr`.`win_side` = 'TERRORIST') THEN `t2`.`name`
            WHEN (`mr`.`win_side` = 'CT') THEN `t`.`name`
        END) AS `winner`
    FROM
        ((((`season_match` `sm`
        JOIN `match_round` `mr` ON ((`mr`.`match_id` = `sm`.`match_id`)))
        JOIN `season` `s` ON ((`sm`.`season_id` = `s`.`season_id`)))
        JOIN `team` `t` ON ((`mr`.`ct_team_id` = `t`.`team_id`)))
        JOIN `team` `t2` ON ((`mr`.`t_team_id` = `t2`.`team_id`)))
    ORDER BY `mr`.`round_id`;