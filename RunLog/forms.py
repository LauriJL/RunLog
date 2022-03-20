from dataclasses import fields
from django import forms
from .models import RunLogModel


class runForms(forms.ModelForm):
    class Meta:
        model = RunLogModel
        fields = "__all__"
