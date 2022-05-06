from django.conf import settings
from django.db import models


class RunLogModel(models.Model):
    run_date = models.DateField()
    distance = models.DecimalField(max_digits=5, decimal_places=2)
    pace = models.DurationField()
    bpm = models.IntegerField()
    remarks = models.TextField(blank=True)
    run_time = models.DurationField()

    def __str__(self):
        return str(self.run_date)

    class Meta:
        db_table = "runlog"


class RunTotalsModel(models.Model):
    average_distance = models.DecimalField(max_digits=5, decimal_places=2)
    total_distance = models.DecimalField(max_digits=5, decimal_places=2)
    furthest_distance = models.DecimalField(max_digits=5, decimal_places=2)
    average_pace = models.DurationField()
    fastest_pace = models.DurationField()
    average_bpm = models.IntegerField()
    average_runtime = models.DurationField()
    goal = models.IntegerField()
    togo = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = "totals"
