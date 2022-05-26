CREATE TRIGGER trigger_totals_cleanup
    AFTER INSERT OR DELETE OR UPDATE 
    ON public.runlog
    FOR EACH ROW
    EXECUTE FUNCTION public.function_clean_totals();