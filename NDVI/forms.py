# forms.py

from django import forms
from .models import MonitoringArea

class MonitoringAreaForm(forms.ModelForm):
    class Meta:
        model = MonitoringArea
        fields = ['name', 'area']
