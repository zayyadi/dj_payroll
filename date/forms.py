from django import forms
from date.widgets import MonthSelectorWidget


class MonthField(forms.DateField):
    widget = MonthSelectorWidget
