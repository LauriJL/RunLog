-- TABLES
-- runlog

CREATE TABLE
IF NOT EXISTS public.runlog
(
    id integer NOT NULL DEFAULT nextval
('runlog_id_seq'::regclass),
    run_date date,
    run_time interval,
    distance numeric
(5,2),
    pace interval,
    bpm integer,
    remarks character varying COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

-- totals

CREATE TABLE
IF NOT EXISTS public.totals
(
    id integer NOT NULL DEFAULT nextval
('totals_id_seq'::regclass),
    average_distance numeric
(5,2) DEFAULT 0.00,
    total_distance numeric
(5,2) DEFAULT 0.00,
    furthest_distance numeric
(5,2) DEFAULT 0.00,
    average_pace time without time zone,
    fastest_pace time without time zone,
    average_bpm integer,
    average_runtime time without time zone
)

TABLESPACE pg_default;

-- FUNCTIONS

CREATE OR REPLACE FUNCTION public.function_totals
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
BEGIN
    SELECT SUM(distance)
    INTO tot_dst
    FROM runlog;
    SELECT AVG(distance)
    INTO avg_dst
    FROM runlog;
    SELECT MAX(distance)
    INTO max_dst
    FROM runlog;
    SELECT AVG(pace)
    INTO avg_pce
    FROM runlog;
    SELECT MIN(pace)
    INTO max_pce
    FROM runlog;
    SELECT AVG(run_time)
    INTO avg_time
    FROM runlog;
    SELECT AVG(bpm)
    INTO avg_bpm
    FROM runlog;
    --RAISE NOTICE 'tot_dst: %', tot_dst;
    UPDATE totals
  SET 
  average_distance = avg_dst,
  total_distance = tot_dst,
  furthest_distance = max_dst,
  average_pace = avg_pce,
  fastest_pace = max_pce,
  average_bpm = avg_bpm,
  average_runtime = avg_time;
    RETURN NEW;
END
$BODY$;

-- SEQUENCES
-- runlog id
CREATE SEQUENCE
IF NOT EXISTS public.runlog_id_seq
    INCREMENT 1
    START 1000
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;
—totals id
CREATE SEQUENCE
IF NOT EXISTS public.totals_id_seq
    INCREMENT 1
    START 2000
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

