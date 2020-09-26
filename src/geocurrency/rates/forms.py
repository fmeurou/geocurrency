from django.forms import ModelForm

from .models import Rate


class RateForm(ModelForm):
    class Meta:
        model = Rate
        exclude = ['user']
