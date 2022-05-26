CREATE OR REPLACE FUNCTION public.function_clean_totals()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
BEGIN
	DELETE FROM totals tot
	WHERE
  	    NOT tot.yr IN (select yr from runlog) OR
  	    tot.yr IS NULL;
	RETURN NULL;
END
$BODY$;
