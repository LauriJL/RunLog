CREATE TRIGGER trigger_totals
    AFTER
INSERT OR
DELETE OR
UPDATE 
    ON public.runlog
    FOR EACH ROW
EXECUTE
FUNCTION public.function_totals
();