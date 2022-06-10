CREATE OR REPLACE FUNCTION public.function_totals_delete
()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
DECLARE avg_dst NUMERIC
(5,2);
DECLARE tot_dst NUMERIC
(5,2);
DECLARE max_dst NUMERIC
(5,2);
DECLARE avg_pce TIME;
DECLARE max_pce TIME;
DECLARE avg_time TIME;
DECLARE avg_bpm INTEGER;
DECLARE yr_a INTEGER;
DECLARE yr_totals INTEGER;
DECLARE username_a VARCHAR;
BEGIN
  SELECT SUM(distance)
  INTO tot_dst
  FROM runlog
  WHERE yr = OLD.yr AND username = OLD.username;
  SELECT AVG(distance)
  INTO avg_dst
  FROM runlog
  WHERE yr = OLD.yr AND username = OLD.username;
  SELECT MAX(distance)
  INTO max_dst
  FROM runlog
  WHERE yr = OLD.yr AND username = OLD.username;
  SELECT AVG(pace)
  INTO avg_pce
  FROM runlog
  WHERE yr = OLD.yr AND username = OLD.username;
  SELECT MIN(pace)
  INTO max_pce
  FROM runlog
  WHERE yr = OLD.yr AND username = OLD.username;
  SELECT AVG(run_time)
  INTO avg_time
  FROM runlog
  WHERE yr = OLD.yr AND username = OLD.username;
  SELECT AVG(bpm)
  INTO avg_bpm
  FROM runlog
  WHERE yr = OLD.yr;
  SELECT (OLD.yr)
  INTO yr_a
  FROM runlog
  WHERE yr = OLD.yr AND username = OLD.username;
  --RAISE NOTICE 'DELETE total_distance %', tot_dst;
  UPDATE totals
  	SET 
  	average_distance = avg_dst,
  	total_distance = tot_dst,
  	furthest_distance = max_dst,
  	average_pace = avg_pce,
  	fastest_pace = max_pce,
  	average_bpm = avg_bpm,
  	average_runtime = avg_time
	WHERE yr = OLD.yr AND username = OLD.username;
  RETURN NEW;
END
$BODY$;