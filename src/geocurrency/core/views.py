from django.shortcuts import render
from django.views.decorators.http import require_safe


@require_safe
def index(request):
    return render(request, 'index.html')


@require_safe
def tos(request):
    return render(request, 'tos.html')