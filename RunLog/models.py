from django.conf import settings
from django.db import models


class RunLogModel(models.Model):
    run_date = models.DateField()
    distance = models.DecimalField(max_digits=5, decimal_places=2)
    pace = models.TimeField()
    bpm = models.IntegerField()
    remarks = models.TextField(blank=True)
    run_time = models.TimeField()
    yr = models.IntegerField()

    @property
    def yr(self):
        return int(self.run_date.strftime('%Y'))

    def __str__(self):
        return str(self.run_date)

    class Meta:
        db_table = "runlog"


class RunTotalsModel(models.Model):
    average_distance = models.DecimalField(max_digits=5, decimal_places=2)
    total_distance = models.DecimalField(max_digits=5, decimal_places=2)
    furthest_distance = models.DecimalField(max_digits=5, decimal_places=2)
    average_pace = models.TimeField()
    fastest_pace = models.TimeField()
    average_bpm = models.IntegerField()
    average_runtime = models.TimeField()
    goal = models.IntegerField()
    yr = models.IntegerField()

    @property
    def togo(self):
        return self.goal - self.total_distance

    def __str__(self):
        return str(self.total_distance)

    class Meta:
        db_table = "totals"
