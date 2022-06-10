CREATE OR REPLACE TRIGGER trigger_totals_delete
    AFTER
DELETE
    ON public.runlog
    FOR EACH
ROW
EXECUTE
FUNCTION public.function_totals_delete
();