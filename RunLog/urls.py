from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.showTotals, name="showTotals"),
    path('log', views.showLog, name="showLog"),
    path('logJSON', views.logJSON, name="logJSON"),
    path('logJSON/<int:id>', views.logJSON_detail, name="logJSON_detail"),
    #path('insert', views.insertRun, name="insertRun"),
    path('addRun', views.addRun),
    path('edit/<id>', views.editRun, name="editRun"),
    path('update/<id>', views.updateRun, name="updateRun"),
    path('delete/<id>/', views.deleteRun, name="deleteRun"),
    path('goal', views.goal, name='goal'),
    #path('toGo', views.goal, name='toGo'),
    # path('addGoal', views.addGoal, name='addGoal'),
    # path('editGoal', views.editGoal, name='editGoal'),
    # path('updateGoal', views.updateGoal, name='updateGoal'),
    path('charts', views.charts, name='charts'),
    path('bpm', views.bpm, name='bpm'),
    path('pace', views.pace, name='pace'),
    path('bpmChart', views.bpm_chart, name='bpmChart'),
    path('distanceChart', views.distance_chart, name='distanceChart'),
    path('paceChart', views.pace_chart, name='paceChart'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
