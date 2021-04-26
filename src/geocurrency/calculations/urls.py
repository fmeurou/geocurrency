"""
Calculations module URLs
"""

from django.urls import path

from .viewsets import ValidateViewSet, CalculationView

app_name = 'calculations'

urlpatterns = [
    path('<str:unit_system>/formulas/validate/', ValidateViewSet.as_view()),
    path('<str:unit_system>/formulas/calculate/', CalculationView.as_view()),
]
