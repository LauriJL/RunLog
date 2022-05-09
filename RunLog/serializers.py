from dataclasses import fields
from rest_framework import serializers
from datetime import datetime
from .models import RunLogModel, RunTotalsModel


class RunLogSerializer(serializers.ModelSerializer):

    run_date = serializers.DateField(format="%d.%m.%Y")
    distance = serializers.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        model = RunLogModel
        fields = '__all__'


class RunTotalSerializer(serializers.ModelSerializer):

    class Meta:
        model = RunTotalsModel
        fields = '__all__'
