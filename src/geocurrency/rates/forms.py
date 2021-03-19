"""
Forms for Rates module
"""
from django.forms import ModelForm

from .models import Rate


class RateForm(ModelForm):
    """
    Rate form
    """
    class Meta:
        """
        Model form
        """
        model = Rate
        exclude = ['user']
