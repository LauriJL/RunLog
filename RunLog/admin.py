from django.contrib import admin
from .models import RunLogModel, RunTotalsModel

admin.site.register(RunLogModel)
admin.site.register(RunTotalsModel)
