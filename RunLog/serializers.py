from dataclasses import fields
from email.policy import default
from rest_framework import serializers
from datetime import datetime
from .models import RunLogModel, RunTotalsModel


class RunLogSerializer(serializers.ModelSerializer):

    run_date = serializers.DateField(format="%d.%m.%Y")
    distance = serializers.DecimalField(max_digits=5, decimal_places=2)
    pace = serializers.TimeField(format="%Mm%Ss")
    run_time = serializers.TimeField(format="%Hh%Mm%Ss")
    yr = serializers.IntegerField()

    class Meta:
        model = RunLogModel
        fields = '__all__'


class RunTotalSerializer(serializers.ModelSerializer):

    average_pace = serializers.TimeField(format="%Mm%Ss")
    fastest_pace = serializers.TimeField(format="%Mm%Ss")
    average_runtime = serializers.TimeField(format="%Hh%Mm%Ss")
    total_distance = serializers.DecimalField(
        max_digits=5, decimal_places=2, default=0.00)
    goal = serializers.IntegerField(default=0)
    togo = serializers.SerializerMethodField('get_togo')

    def get_togo(self, obj):
        if obj.total_distance == None:
            obj.total_distance = 0
        return obj.goal - obj.total_distance

    class Meta:
        model = RunTotalsModel
        fields = '__all__'


class dateSerializer(serializers.ModelSerializer):
    #run_date = serializers.DateField(format="%Y")
    #run_date = serializers.SerializerMethodField('get_yr')
    run_date = serializers.DateField()

    def get_yr(self, obj):
        return obj.run_date.year

    class Meta:
        model = RunLogModel
        #fields = ('run_date', )
        fields = '__all__'
