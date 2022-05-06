from cProfile import label
from django.http import HttpResponse, JsonResponse
from .models import RunLogModel, RunTotalsModel
from .serializers import RunLogSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import runForms


def showTotals(request):
    showall = RunTotalsModel.objects.all()
    return render(request, 'totals.html', {"dataTotals": showall})


def showLog(request):
    showall = RunLogModel.objects.all().order_by('run_date')
    return render(request, 'log.html', {"dataLog": showall})


@api_view(['GET', 'POST'])
def logJSON(request, format=None):
    if request.method == 'GET':
        showall = RunLogModel.objects.all().order_by('run_date')
        serializer = RunLogSerializer(showall, many=True)
        return render(request, 'logJSON.html', {"dataLog": serializer.data})
    if request.method == 'POST':
        serializer = RunLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def logJSON_detail(request, id):

    try:
        run = RunLogModel.objects.get(pk=id)
    except RunLogModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RunLogSerializer(run)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = RunLogSerializer(run, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        run.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # def insertRun(request):
    #     if request.method == "POST":
    #         if request.POST.get('run_date') and request.POST.get('run_time') and request.POST.get('distance') and request.POST.get('pace') and request.POST.get('bpm') and request.POST.get('remarks'):
    #             saverecord = RunLogModel()
    #             saverecord.run_date = request.POST.get('run_date')
    #             saverecord.run_time = request.POST.get('run_time')
    #             saverecord.distance = request.POST.get('distance')
    #             saverecord.pace = request.POST.get('pace')
    #             saverecord.bpm = request.POST.get('bpm')
    #             saverecord.remarks = request.POST.get('remarks')
    #             saverecord.save()
    #             messages.success(request, 'Run on ' +
    #                              saverecord.run_date + ' added successfully.')
    #             return render(request, 'log.html')
    #     else:
    #         return render(request, 'log.html')


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
            remarks=remarks
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
        messages.success(request, 'Run updated OK')
        return render(request, 'edit.html', {'RunLogModel': updaterun})


def deleteRun(request, id):
    run = RunLogModel.objects.get(id=id)
    run.delete()
    return redirect('showLog')


def goal(request):
    #showall = RunTotalsModel.objects.all()
    # return render(request, 'goal.html', {"goal": showall}, {})
    showall = RunTotalsModel.objects.all()
    return render(request, 'goal.html', {"dataTotals": showall})


def addGoal(request):
    if request.method == 'POST':
        goal = request.POST['goal']

    RunTotalsModel.objects.create(
        goal=goal
    )

    return render(request, 'addGoal.html')


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
        'bpm', 'run_date').order_by('run_date')

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
        'distance', 'run_date').order_by('run_date')
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
        'pace', 'run_date').order_by('run_date')

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
