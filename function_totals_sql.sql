CREATE OR REPLACE FUNCTION public.function_totals()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
DECLARE avg_dst NUMERIC(5,2);
DECLARE tot_dst NUMERIC(5,2);
DECLARE max_dst NUMERIC(5,2);
DECLARE avg_pce TIME;
DECLARE max_pce TIME;
DECLARE avg_time TIME;
DECLARE avg_bpm INTEGER;
DECLARE yr_a INTEGER;
BEGIN
  SELECT SUM(distance) INTO tot_dst
  FROM runlog
  WHERE yr = new.yr;
  SELECT AVG(distance) INTO avg_dst
  FROM runlog
  WHERE yr = new.yr;
  SELECT MAX(distance) INTO max_dst
  FROM runlog
  WHERE yr = new.yr;
  SELECT AVG(pace) INTO avg_pce
  FROM runlog
  WHERE yr = new.yr;
  SELECT MIN(pace) INTO max_pce
  FROM runlog
  WHERE yr = new.yr;
  SELECT AVG(run_time) INTO avg_time
  FROM runlog
  WHERE yr = new.yr;
  SELECT AVG(bpm) INTO avg_bpm
  FROM runlog
  WHERE yr = new.yr;
  SELECT (NEW.yr) INTO yr_a
  FROM runlog
  WHERE yr = new.yr;
  IF NOT EXISTS (SELECT * FROM totals WHERE yr = new.yr) THEN
  	INSERT INTO totals 
		(average_distance, total_distance, furthest_distance, average_pace, fastest_pace, average_bpm, average_runtime, yr) 
	  VALUES (avg_dst, tot_dst, max_dst, avg_pce, max_pce, avg_bpm, avg_time, yr_a);
	  RETURN NEW;
  ELSEIF EXISTS (SELECT * FROM totals WHERE yr = new.yr) THEN
  	UPDATE totals
  	SET
  	  average_distance = avg_dst,
  	  total_distance = tot_dst,
  	  furthest_distance = max_dst,
  	  average_pace = avg_pce,
  	  fastest_pace = max_pce,
  	  average_bpm = avg_bpm,
  	  average_runtime = avg_time,
  	  yr = yr_a
	  WHERE yr = new.yr;
  	RETURN NEW;
  ELSEIF (SELECT * FROM totals WHERE yr IS NULL) THEN
    DELETE from totals
	  WHERE yr IS NULL;
	  RETURN NULL;
    END IF;
END
$BODY$;