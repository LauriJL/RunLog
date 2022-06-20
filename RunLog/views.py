import datetime
from datetime import date
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import RunLogModel, RunTotalsModel
from .serializers import RunLogSerializer, RunTotalSerializer, dateSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import runForms, totalForms
from django.shortcuts import render
from django.contrib.auth import get_user_model

# Globals
currentYear = int(datetime.date.today().year)
firstDay = date(date.today().year, 1, 1)
lastDay = date(date.today().year, 12, 31)


def index(request):
    return render(request, 'index.html')


def showTotals(request):
    showall = RunTotalsModel.objects.all()
    return render(request, 'totals.html', {"dataTotals": showall})


def showLog(request):
    showall = RunLogModel.objects.all().order_by('run_date')
    paginator = Paginator(showall, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'log.html', {"page_obj": page_obj})
    # return render(request, 'log.html', {"dataLog": showall})


@api_view(['GET', 'POST'])
def logJSON(request):
    if request.method == 'GET':
        showall = RunLogModel.objects.filter(username=request.user,
                                             run_date__range=[firstDay, lastDay]).order_by('run_date')
        serializer = RunLogSerializer(showall, many=True)
        # return JsonResponse({'runs': serializer.data})
        return render(request, 'logJSON.html', {'dataLogJSON': serializer.data})
    if request.method == 'POST':
        serializer = RunLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def totalsJSON(request):
    if request.method == 'GET':
        showTotals = RunTotalsModel.objects.filter(
            username=request.user, yr=currentYear)
        serializer = RunTotalSerializer(showTotals, many=True)
        return render(request, 'totalsJSON.html', {'dataTotalsJSON': serializer.data})
        # return JsonResponse({'totals': serializer.data})


def addRun(request):
    if request.method == 'POST':
        run_date = request.POST['run_date']
        run_time = request.POST['run_time']
        distance = request.POST['distance']
        pace = request.POST['pace']
        bpm = request.POST['bpm']
        remarks = request.POST['remarks']

        RunLogModel.objects.create(
            run_date=run_date,
            run_time=run_time,
            distance=distance,
            pace=pace,
            bpm=bpm,
            remarks=remarks,
            username=request.user,
        )

        return render(request, 'log.html')


def editRun(request, id):
    editrun = RunLogModel.objects.get(id=id)
    return render(request, 'edit.html', {'RunLogModel': editrun})


def updateRun(request, id):
    updaterun = RunLogModel.objects.get(id=id)
    form = runForms(request.POST, instance=updaterun)
    if form.is_valid():
        form.save()
        # messages.success(request, 'Run updated.')
        # return render(request, 'edit.html', {'RunLogModel': updaterun})
        return redirect('showLog')


def deleteRun(request, id):
    run = RunLogModel.objects.get(id=id)
    run.delete()
    return redirect('showLog')


def goal(request):
    showall = RunTotalsModel.objects.filter(
        username=request.user, yr=currentYear)
    return render(request, 'goal.html', {"dataTotals": showall})


def addGoal(request):
    #editgoal = RunTotalsModel.objects.get(id=id)
    return render(request, 'addGoal.html', {})


def addNewGoal(request):
    if request.method == 'POST':
        goal = request.POST["goal"]
        yr = currentYear
        username = request.user

        RunTotalsModel.objects.create(
            goal=goal,
            yr=yr,
            username=username,
        )

        return redirect('goal')


def editGoal(request, id):
    editgoal = RunTotalsModel.objects.get(id=id)
    return render(request, 'editGoal.html', {'RunTotalsModel': editgoal})


def updateGoal(request, id):
    updategoal = RunTotalsModel.objects.get(id=id)
    form = totalForms(request.POST, instance=updategoal)
    if form.is_valid():
        form.save()
        return redirect('goal')


def charts(request):
    return render(request, 'charts.html')


def bpm(request):
    return render(request, 'bpm.html')


def pace(request):
    return render(request, 'pace.html')


def bpm_chart(request):
    labels = []
    data = []

    queryset = RunLogModel.objects.values(
        'bpm', 'run_date').filter(username=request.user,
                                  run_date__range=[firstDay, lastDay]).order_by('run_date')

    for item in queryset:
        labels.append(item['run_date'])
        data.append(item['bpm'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def distance_chart(request):
    labels = []
    data = []

    queryset = RunLogModel.objects.values(
        'distance', 'run_date').filter(username=request.user,
                                       run_date__range=[firstDay, lastDay]).order_by('run_date')
    for item in queryset:
        labels.append(item['run_date'])
        data.append(item['distance'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def pace_chart(request):
    labels = []
    rawdata = []
    data = []

    queryset = RunLogModel.objects.values(
        'pace', 'run_date').filter(username=request.user,
                                   run_date__range=[firstDay, lastDay]).order_by('run_date')

    for item in queryset:
        labels.append(item['run_date'])
        rawdata.append(item['pace'])

    str1 = ','.join(str(e) for e in rawdata)
    str2 = str1.split(',')

    data = [i.replace('0:', '') for i in str2]
    data = [i.replace(':', '.') for i in data]

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def goal_chart(request):
    goal = []
    total_distance = []

    queryset = RunTotalsModel.objects.values(
        'goal', 'total_distance').filter(username=request.user, yr=currentYear)
    for item in queryset:
        goal.append(item['goal'])
        total_distance.append(item['total_distance'])

    return JsonResponse(data={
        'goal': goal,
        'total_distance': total_distance,
    })


def combined_chart(request):
    raw_pace = []
    pace = []
    bpm = []
    distance = []
    labels = []

    queryset = RunLogModel.objects.values(
        'pace', 'bpm', 'distance', 'run_date').filter(username=request.user,
                                                      run_date__range=[firstDay, lastDay]).order_by('run_date')

    for item in queryset:
        labels.append(item['run_date'])
        raw_pace.append(item['pace'])
        bpm.append(item['bpm'])
        distance.append(item['distance'])

    str1 = ','.join(str(e) for e in raw_pace)
    str2 = str1.split(',')

    pace = [i.replace('0:', '') for i in str2]
    pace = [i.replace(':', '.') for i in pace]

    return JsonResponse(data={
        'labels': labels,
        'pace': pace,
        'bpm': bpm,
        'distance': distance
    })


def getYears(request):
    if request.method == 'GET':
        showYears = RunLogModel.objects.all().distinct('run_date')
        serializer = dateSerializer(showYears, many=True)
        # return JsonResponse({'years': serializer.data})
        return render(request, 'years.html', {'showYears': serializer.data})


def archiveTotals(request):
    if request.method == 'GET':
        showTotals = RunTotalsModel.objects.all().filter(yr__lt=currentYear)
        serializer = RunTotalSerializer(showTotals, many=True)
        return render(request, 'archiveTotals.html', {'dataArchiveTotals': serializer.data})
        # return JsonResponse({'totalsArchive': serializer.data})


def archiveLogs(request):
    if request.method == 'GET':
        showall = RunLogModel.objects.filter(
            run_date__lte=firstDay).order_by('run_date')
        serializer = RunLogSerializer(showall, many=True)
        # return JsonResponse({'archivedRuns': serializer.data})
        return render(request, 'archiveLogs.html', {'dataArchiveLog': serializer.data})


def archiveCharts(request):
    return render(request, 'archiveCharts.html')


def archive_chart(request):
    raw_pace = []
    pace = []
    bpm = []
    distance = []
    labels = []

    queryset = RunLogModel.objects.values(
        'pace', 'bpm', 'distance', 'run_date').filter(
            run_date__lte=firstDay).order_by('run_date')

    for item in queryset:
        labels.append(item['run_date'])
        raw_pace.append(item['pace'])
        bpm.append(item['bpm'])
        distance.append(item['distance'])

    str1 = ','.join(str(e) for e in raw_pace)
    str2 = str1.split(',')

    pace = [i.replace('0:', '') for i in str2]
    pace = [i.replace(':', '.') for i in pace]

    return JsonResponse(data={
        'labels': labels,
        'pace': pace,
        'bpm': bpm,
        'distance': distance
    })
