CREATE TABLE IF NOT EXISTS public.totals
(
    id integer NOT NULL DEFAULT nextval('totals_id_seq'::regclass),
    average_distance numeric(5,2) DEFAULT 0.00,
    total_distance numeric(5,2) DEFAULT 0.00,
    furthest_distance numeric(5,2) DEFAULT 0.00,
    average_pace time without time zone,
    fastest_pace time without time zone,
    average_bpm integer,
    average_runtime time without time zone,
    goal integer,
    togo numeric(5,2) GENERATED ALWAYS AS (((goal)::numeric - total_distance)) STORED
)