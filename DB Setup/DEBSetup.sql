DROP TABLE IF EXISTS geek.geekfest_match_award;
DROP TABLE IF EXISTS geek.geekfest_award;
DROP TABLE IF EXISTS geek.award_category;
DROP TABLE IF EXISTS geek.match_award;
DROP TABLE IF EXISTS geek.grenade_toss;
DROP TABLE IF EXISTS geek.blind;
DROP TABLE IF EXISTS geek.assist;
DROP TABLE IF EXISTS geek.buy;
DROP TABLE IF EXISTS geek.team_event_action;
DROP TABLE IF EXISTS geek.player_event_action;
DROP TABLE IF EXISTS geek.action;
DROP TABLE IF EXISTS geek.death;
DROP TABLE IF EXISTS geek.frag;
DROP TABLE IF EXISTS geek.item;
DROP TABLE IF EXISTS geek.match_round;
DROP TABLE IF EXISTS geek.season_match;
DROP TABLE IF EXISTS geek.team_geek;
DROP TABLE IF EXISTS geek.team;
DROP TABLE IF EXISTS geek.geek;
DROP TABLE IF EXISTS geek.generation;
DROP TABLE IF EXISTS geek.tier;
DROP TABLE IF EXISTS geek.season;


CREATE TABLE geek.tier(
	tier_id				INT				NOT NULL	auto_increment
    , tier_name			VARCHAR(250)	NOT NULL
    , tier_description	TEXT			NULL
	, PRIMARY KEY (tier_id)
);

CREATE TABLE geek.generation(
	generation_id		INT				NOT NULL	auto_increment
    , generation_name	VARCHAR(250)	NOT NULL
    , gen_description	TEXT			NULL
    , PRIMARY KEY (generation_id)
);


CREATE TABLE geek.geek(
	geek_id 			INT 			NOT NULL 	auto_increment
    , csgo_id 			VARCHAR(100) 	NOT NULL
    , handle 			VARCHAR(250) 	NULL
    , first_name 		VARCHAR(250) 	NULL
    , last_name 		VARCHAR(250)	NULL
    , location			VARCHAR(20)		NULL
    , occupation		VARCHAR(250)	NULL
    , member_since		date			NULL
    , tier_id			INT				NULL
    , generation_id		INT				NULL
    , is_member			BOOL			NULL 	DEFAULT false
    , PRIMARY KEY (geek_id)
    , FOREIGN KEY (tier_id) REFERENCES geek.tier(tier_id)
    , FOREIGN KEY (generation_id) REFERENCES geek.generation(generation_id)
);

CREATE TABLE geek.season(
	season_id			INT				NOT NULL	auto_increment
    , name				VARCHAR(250)	NOT NULL
    , start_date		DATETIME		NOT NULL
    , end_date			DATETIME		NULL
    , PRIMARY KEY (season_id)
);

CREATE TABLE geek.team(
	team_id				INT				NOT NULL	auto_increment
	, season_id			INT				NOT NULL
    , name				VARCHAR(250)	NOT NULL
    , description		VARCHAR(5000)	NULL
    , captain_id		INT				NOT NULL
    , co_captain_id		INT				NOT NULL
    , PRIMARY KEY (team_id)
    , FOREIGN KEY (captain_id) REFERENCES geek.geek(geek_id)
    , FOREIGN KEY (co_captain_id) REFERENCES geek.geek(geek_id)
    , FOREIGN KEY (season_id) REFERENCES geek.season(season_id)
);

CREATE TABLE geek.team_geek(
    geek_id				INT				NOT NULL	
    , team_id			INT				NOT NULL
    , PRIMARY KEY (geek_id, team_id)
    , FOREIGN KEY (geek_id) REFERENCES geek.geek(geek_id)
    , FOREIGN KEY (team_id) REFERENCES geek.team(team_id)
);

CREATE TABLE geek.season_match(
	match_id			INT				NOT NULL	auto_increment
    , match_date		DATETIME		NOT NULL
    , season_id			INT				NULL
    , map				VARCHAR(200)	NOT NULL
    , team_winner		INT				NULL
    , PRIMARY KEY (match_id)
    , FOREIGN KEY (team_winner) REFERENCES geek.team(team_id)
    , FOREIGN KEY (season_id) REFERENCES geek.season(season_id)
);

CREATE TABLE geek.match_round(
	round_id			INT				NOT NULL	auto_increment
    , match_id			INT				NOT NULL
    , ct_team_id		INT				NULL
    , t_team_id			INT				NULL
    , win_side			VARCHAR(100)	NULL
    , PRIMARY KEY (round_id)
    , FOREIGN KEY (match_id) REFERENCES geek.season_match(match_id)
    , FOREIGN KEY (ct_team_id) REFERENCES geek.team(team_id)
    , FOREIGN KEY (t_team_id) REFERENCES geek.team(team_id)
);

CREATE TABLE geek.item(
	item_id				INT				NOT NULL	auto_increment
    , name				VARCHAR(1000)	NOT NULL
    , decscription		VARCHAR(1000)	NOT NULL
    , cost				DECIMAL(12,4) 	NULL
    , category			VARCHAR(100)	NULL
    , sub_category		VARCHAR(100)	NULL
    , PRIMARY KEY (item_id)
);

CREATE TABLE geek.frag(
	frag_id				INT				NOT NULL auto_increment
    , geek_id			INT				NOT NULL
    , round_id			INT				NOT NULL
    , victim_id			INT				NOT NULL
    , pos_x				DECIMAL(12,4)	NOT NULL
    , pos_y				DECIMAL(12,4)	NOT NULL
    , pos_z				DECIMAL(12,4)	NOT NULL
    , pos_victim_x		DECIMAL(12,4)	NOT NULL
    , pos_victim_y		DECIMAL(12,4)	NOT NULL
    , pos_victim_z		DECIMAL(12,4)	NOT NULL
	, distance			DECIMAL(12,4)	NOT NULL
    , is_headshot		BOOL			NOT NULL DEFAULT false
    , is_penetration	BOOL			NOT NULL DEFAULT false
    , is_teamkill		bool			NOT NULL DEFAULT false
    , item_id			INT				NOT NULL
    , PRIMARY KEY (frag_id)
    , FOREIGN KEY (round_id) REFERENCES geek.match_round(round_id) ON DELETE CASCADE
    , FOREIGN KEY (geek_id) REFERENCES geek.geek(geek_id)
    , FOREIGN KEY (victim_id) REFERENCES geek.geek(geek_id)
    , FOREIGN KEY (item_id) REFERENCES geek.item(item_id)
);

CREATE TABLE geek.death(
	death_id			INT				NOT NULL auto_increment
    , geek_id			INT				NOT NULL
    , round_id			INT				NOT NULL
    , killer_id			INT				NULL
    , pos_x				DECIMAL(12,4)	NOT NULL
    , pos_y				DECIMAL(12,4)	NOT NULL
    , pos_z				DECIMAL(12,4)	NOT NULL
    , pos_killer_x		DECIMAL(12,4)	NOT NULL
    , pos_killer_y		DECIMAL(12,4)	NOT NULL
    , pos_killer_z		DECIMAL(12,4)	NOT NULL
	, distance			DECIMAL(12,4)	NOT NULL
    , is_headshot		BOOL			NOT NULL DEFAULT false
    , is_penetration	BOOL			NOT NULL DEFAULT false
    , is_teamkill		bool			NOT NULL DEFAULT false
    , item_id			INT				NOT NULL
    , PRIMARY KEY (death_id)
    , FOREIGN KEY (round_id) REFERENCES geek.match_round(round_id) ON DELETE CASCADE
    , FOREIGN KEY (geek_id) REFERENCES geek.geek(geek_id)
    , FOREIGN KEY (killer_id) REFERENCES geek.geek(geek_id)
    , FOREIGN KEY (item_id) REFERENCES geek.item(item_id)
);

CREATE TABLE geek.action(
	action_id			INT				NOT NULL auto_increment
    , code				VARCHAR(100)	NOT NULL
    , player_points		INT				NULL
    , team_points		INT				NULL
    , team				VARCHAR(50)		NULL
    , description		VARCHAR(1000)	NULL
    , PRIMARY KEY (action_id)
);

CREATE TABLE geek.player_event_action(
	player_event_action_id	INT				NOT NULL auto_increment
    , event_time		DATETIME		NULL
    , round_id			INT				NOT NULL
    , geek_id			INT				NOT NULL
    , action_id			INT				NOT NULL
    , PRIMARY KEY (player_event_action_id)
    , FOREIGN KEY (round_id) REFERENCES geek.match_round(round_id) ON DELETE CASCADE
    , FOREIGN KEY (geek_id) REFERENCES geek.geek(geek_id)
    , FOREIGN KEY (action_id) REFERENCES geek.action(action_id)
);

CREATE TABLE geek.team_event_action(
	team_event_action_id	INT				NOT NULL auto_increment
	, event_time		DATETIME		NULL
    , round_id			INT				NOT NULL
    , team_id			INT				NULL
    , action_id			INT				NOT NULL
    , PRIMARY KEY (team_event_action_id)
    , FOREIGN KEY (round_id) REFERENCES geek.match_round(round_id) ON DELETE CASCADE
    , FOREIGN KEY (team_id) REFERENCES geek.team(team_id)
    , FOREIGN KEY (action_id) REFERENCES geek.action(action_id)
);

CREATE TABLE geek.buy(
	buy_id				INT				NOT NULL auto_increment
    , round_id			INT				NOT NULL
    , geek_id			INT				NOT NULL
    , item_id			INT				NOT NULL
    , PRIMARY KEY (buy_id)
    , FOREIGN KEY (round_id) REFERENCES geek.match_round(round_id) ON DELETE CASCADE
    , FOREIGN KEY (geek_id) REFERENCES geek.geek(geek_id)
    , FOREIGN KEY (item_id) REFERENCES geek.item(item_id)
);

CREATE TABLE geek.assist(
	assist_id			INT				NOT NULL auto_increment
    , round_id			INT				NOT NULL
    , geek_id			INT				NOT NULL
    , killing_player_id	INT				NULL
    , is_tk_assist		BOOL			NOT NULL default FALSE
    , PRIMARY KEY (assist_id)
    , FOREIGN KEY (round_id) REFERENCES geek.match_round(round_id) ON DELETE CASCADE
    , FOREIGN KEY (geek_id) REFERENCES geek.geek(geek_id)
    , FOREIGN KEY (killing_player_id) REFERENCES geek.geek(geek_id)
);

CREATE TABLE geek.blind(
	blind_id			INT				NOT NULL auto_increment
    , round_id			INT 			NOT NULL
    , blinding_player_id INT			NOT NULL
    , blinded_player_id	INT				NOT NULL
    , is_team_blind		bool			NOT NULL default FALSE
    , duration			DECIMAL(12,4)	NOT NULL
    , PRIMARY KEY (blind_id)
    , FOREIGN KEY (round_id) REFERENCES geek.match_round(round_id) ON DELETE CASCADE
    , FOREIGN KEY (blinding_player_id) REFERENCES geek.geek(geek_id)
    , FOREIGN KEY (blinded_player_id) REFERENCES geek.geek(geek_id)
);

CREATE TABLE geek.grenade_toss(
	grenade_toss_id		INT				NOT NULL auto_increment
    , round_id			INT				NOT NULL
    , geek_id			INT				NOT NULL
    , item_id			INT				NOT NULL
    , pos_x				DECIMAL(12,4)	NULL
    , pos_y				DECIMAL(12,4) 	NULL
    , pos_z				DECIMAL(12,4)	NULL
    , PRIMARY KEY (grenade_toss_id)
    , FOREIGN KEY (round_id) REFERENCES geek.match_round(round_id) ON DELETE CASCADE
    , FOREIGN KEY (geek_id) REFERENCES geek.geek(geek_id)
    , FOREIGN KEY (item_id) REFERENCES geek.item(item_id)
);

CREATE TABLE geek.match_award(
	match_award_id		INT				NOT NULL auto_increment
    , match_id			INT				NOT NULL
    , geek_id			INT				NOT NULL
    , award_name		VARCHAR(1000)	NOT NULL
    , award_value		DECIMAL(12,4)	NULL
    , award_position	INT				NULL
    , score				DECIMAL(12,4)	NULL
    , PRIMARY KEY (match_award_id)
    , FOREIGN KEY (match_id) REFERENCES geek.season_match(match_id)
	, FOREIGN KEY (geek_id) REFERENCES geek.geek(geek_id)
);

CREATE TABLE geek.award_category(
	award_category_id	INT				NOT NULL auto_increment
    , category_name		VARCHAR(1000)	NOT NULL
    , category_description VARCHAR(1000) NOT NULL
    , PRIMARY KEY (award_category_id)
);

CREATE TABLE geek.geekfest_award(
	geekfest_award_id	INT				NOT NULL auto_increment
    , award_name		VARCHAR(1000)	NOT NULL
    , award_title		VARCHAR(1000)	NOT NULL
    , award_description	VARCHAR(1000)	NULL
    , award_image_path	VARCHAR(1000)	NULL
    , award_category_id	INT				NOT NULL
    , award_query		VARCHAR(20000)	NOT NULL
    , award_query_type	VARCHAR(100)	NOT NULL
    , PRIMARY KEY (geekfest_award_id)
    , FOREIGN KEY (award_category_id) REFERENCES geek.award_category(award_category_id)
);

CREATE TABLE geek.geekfest_match_award(
	geekfest_match_award_id	INT			NOT NULL auto_increment
    , match_id			INT				NOT NULL
    , geekfest_award_id	INT				NOT NULL
    , geek_id			INT				NOT NULL
    , award_rank		INT				NOT NULL
    , award_value		DECIMAL(12,4)	NOT NULL
    , PRIMARY KEY (geekfest_match_award_id)
    , FOREIGN KEY (match_id) REFERENCES geek.season_match(match_id) ON DELETE CASCADE
    , FOREIGN KEY (geekfest_award_id) REFERENCES geek.geekfest_award(geekfest_award_id) ON DELETE CASCADE
    , FOREIGN KEY (geek_id) REFERENCES geek.geek(geek_id) ON DELETE CASCADE
);
