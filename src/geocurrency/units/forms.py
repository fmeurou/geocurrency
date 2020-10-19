from django.forms import ModelForm

from .models import CustomUnit


class CustomUnitForm(ModelForm):
    class Meta:
        model = CustomUnit
        exclude = ['user', 'unit_system']
