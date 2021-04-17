import datetime
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from .models import Table, Week
from .scheduler import create_matchups


def index(request):
    week = Week.objects.order_by('-start').first()
    weeks = Week.objects.order_by('-start')
    tables = Table.objects.filter(week=week).select_related().all()
    context = {
        'week': week,
        'weeks': weeks,
        'tables': tables,
    }
    return render(request, 'base.html', context)
