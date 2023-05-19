truncate table season_player_tiers;

insert into season_player_tiers (season_id, player, tier, total_kills, total_deaths, total_assists, season_KDR)
SELECT 25, player, tier, sum(kills), sum(deaths), sum(assists), round(sum(kills)/sum(deaths),2) as KDR 
FROM geek.tiers_data where matchdate > '2023-01-31' and matchdate  <='2023-03-02'
GROUP BY player, tier;

update season_player_tiers spt
inner join geek g on spt.player = g.handle
set spt.player_id  = geek_id;

update season_player_tiers spt
inner join tier t on spt.tier = t.tier_name
set spt.tier_id  = t.tier_id;
