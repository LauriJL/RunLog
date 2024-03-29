from django.contrib import admin
from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    #path('pwd', views.change_password, name='change_password'),
    path('logJSON', views.logJSON, name="showLog"),
    # path('logJSON', views.logJSON),
    path('totalsJSON', views.totalsJSON, name='totalsJSON'),
    path('addRun', views.addRun),
    path('edit/<id>', views.editRun, name="editRun"),
    path('update/<id>', views.updateRun, name="updateRun"),
    path('show/<id>', views.showRun, name='showRun'),
    path('delete/<id>/', views.deleteRun, name="deleteRun"),
    path('goal', views.goal, name='goal'),
    path('addGoal', views.addGoal, name='addGoal'),
    path('addNewGoal', views.addNewGoal),
    path('editGoal/<id>', views.editGoal, name='editGoal'),
    path('updateGoal/<id>', views.updateGoal, name='updateGoal'),
    path('charts', views.charts, name='charts'),
    path('bpm', views.bpm, name='bpm'),
    path('pace', views.pace, name='pace'),
    path('bpmChart', views.bpm_chart, name='bpmChart'),
    path('distanceChart', views.distance_chart, name='distanceChart'),
    path('paceChart', views.pace_chart, name='paceChart'),
    path('goalChart', views.goal_chart, name='goalChart'),
    path('combinedChart', views.combined_chart, name='combinedChart'),
    path('archiveTotals', views.archiveTotals, name='archiveTotals'),
    path('archiveLogs', views.archiveLogs, name='archiveLogs'),
    path('editArchive/<id>', views.editRunArchive, name="editRunArchive"),
    path('updateRunArchive/<id>', views.updateRunArchive, name="updateRunArchive"),
    path('archiveCharts', views.archiveCharts, name='archiveCharts'),
    path('archiveChartData', views.archive_chart, name='archiveChartData'),
    path('users/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls')),
    path('years', views.getYears, name='years')
]

urlpatterns = format_suffix_patterns(urlpatterns)
