CREATE TABLE IF NOT EXISTS public.runlog
(
    id integer NOT NULL DEFAULT nextval('runlog_id_seq'::regclass),
    run_date date,
    run_time time without time zone,
    distance numeric(5,2),
    pace time without time zone,
    bpm integer,
    remarks character varying COLLATE pg_catalog."default",
    yr integer GENERATED ALWAYS AS (date_part('year'::text, run_date)) STORED
)