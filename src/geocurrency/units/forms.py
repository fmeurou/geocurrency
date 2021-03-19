"""
Units module forms
"""

from django.forms import ModelForm, CharField

from .models import CustomUnit


class CustomUnitForm(ModelForm):
    key = CharField(max_length=255, required=False)
    symbol = CharField(max_length=20, required=False)
    alias = CharField(max_length=20, required=False)

    class Meta:
        model = CustomUnit
        exclude = ['user', 'unit_system']
