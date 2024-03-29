from dataclasses import fields
from django import forms
from .models import RunLogModel, RunTotalsModel
from django.forms import ModelForm, ValidationError


class runForms(forms.ModelForm):
    class Meta:
        model = RunLogModel
        fields = "__all__"


class totalForms(forms.ModelForm):
    class Meta:
        model = RunTotalsModel
        fields = 'goal',
