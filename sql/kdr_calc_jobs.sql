CREATE PROCEDURE `kdr_history_calc` ()
BEGIN

-- Calculate the all time KDR
    update geek.geek g
    set g.alltime_kdr = (
	select round(sum(t.kills)/sum(t.deaths),2) as KDR
	from geek.tiers_data t
	where t.geekid = g.geek_id
	group by t.geekid, t.player );

-- Calculate the 1 year KDR
	update geek
    set geek.year_kdr = (
	select round(sum(kills)/sum(deaths),2) as KDR
    from tiers_data
    where matchdate > CURDATE() - INTERVAL 365 DAY
    and tiers_data.geekid = geek.geek_id);

-- Calculate the 90 day KDR
	update geek
    set geek.last90_kdr = (
	select round(sum(kills)/sum(deaths),2) as KDR
    from tiers_data
    where matchdate > CURDATE() - INTERVAL 90 DAY
    and tiers_data.geekid = geek.geek_id);

-- Insert the newly calculated values into the history table with the current date
	insert into geek_kdr_history(geek_id, handle, history_date, alltime_kdr, year_kdr, last90_kdr)
	select geek_id, handle, CURDATE(), alltime_kdr, year_kdr, last90_kdr
	from geek
	where last90_kdr is not null      ;
                                                 
-- Log the date that this procedure was run in the geeks table for troubleshooting
	update geek.geek g
	set g.last_kdr_update = CURDATE();
    
    select * from geek.geek;
END

CREATE EVENT kdr_history_calc
ON SCHEDULE EVERY 1 WEEK
STARTS CURRENT_TIMESTAMP + INTERVAL 16 HOUR
DO
	CALL `geek`.`kdr_history_calc`();